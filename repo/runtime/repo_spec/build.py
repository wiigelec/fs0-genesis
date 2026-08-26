from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SHA40_RE = re.compile(r"^[0-9a-f]{40}$")


class BuildError(ValueError):
    pass


@dataclass(frozen=True)
class BuildContext:
    plan_directory: Path
    plan_id: str
    candidate_revision: str
    authorized_mutation_paths: tuple[str, ...]


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise BuildError(f"unable to load runtime module: {path}")
    module = importlib.util.module_from_spec(spec)
    old = sys.dont_write_bytecode
    runtime_dir = str(path.parent.resolve())
    added_path = False
    if runtime_dir not in sys.path:
        sys.path.insert(0, runtime_dir)
        added_path = True
    sys.dont_write_bytecode = True
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old
        if added_path and sys.path and sys.path[0] == runtime_dir:
            sys.path.pop(0)
    return module


def _require_sha(value: str, label: str) -> None:
    if not isinstance(value, str) or not SHA40_RE.fullmatch(value):
        raise BuildError(f"{label} must be exact 40-hex repository revision")


def load_exactly_one_accepted_plan(
    root: Path,
    plan_directory: Path,
    *,
    accepted_plan_id: str,
) -> BuildContext:
    # Build consumes exactly one accepted Plan. Acceptance identity is supplied by
    # Governance; Build validates that the loaded Plan is the same bounded Plan.
    plan_runtime = _load_module(
        root / "repo/runtime/repo_spec/plan.py",
        "fs0_build_plan",
    )
    loaded = plan_runtime.validate_plan(root, plan_directory)

    plan_id = loaded.root.get("plan_id")
    if not isinstance(plan_id, str) or not plan_id:
        raise BuildError("loaded Plan lacks stable identity")
    if accepted_plan_id != plan_id:
        raise BuildError(
            f"accepted Plan identity mismatch: expected {accepted_plan_id}, loaded {plan_id}"
        )

    candidate = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if candidate.returncode != 0:
        raise BuildError(f"unable to resolve candidate repository revision: {candidate.stderr.strip()}")
    candidate_revision = candidate.stdout.strip()
    _require_sha(candidate_revision, "candidate revision")

    authorized = tuple(plan_runtime.authorized_mutation_set(loaded))
    return BuildContext(
        plan_directory=plan_directory.resolve(),
        plan_id=plan_id,
        candidate_revision=candidate_revision,
        authorized_mutation_paths=authorized,
    )


def reject_mutations_outside_authorized_set(
    context: BuildContext,
    observed_paths: list[str] | tuple[str, ...],
) -> None:
    authorized = set(context.authorized_mutation_paths)
    outside = sorted({path for path in observed_paths if path not in authorized})
    if outside:
        raise BuildError(f"observed mutation outside accepted Plan authorization: {outside}")


def mutation_manifest(
    context: BuildContext,
    observed_paths: list[str] | tuple[str, ...],
) -> dict:
    reject_mutations_outside_authorized_set(context, observed_paths)
    return {
        "schema_version": "1",
        "record_type": "build-mutation-manifest",
        "accepted_plan_id": context.plan_id,
        "candidate_revision": context.candidate_revision,
        "authorized_mutation_paths": list(context.authorized_mutation_paths),
        "observed_mutation_paths": list(observed_paths),
    }


def verify_syntax(root: Path) -> dict:
    checked_python = []
    checked_json = []
    for path in sorted((root / "repo").rglob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        checked_python.append(str(path.relative_to(root)))
    for path in sorted(root.rglob("*.json")):
        json.loads(path.read_text(encoding="utf-8"))
        checked_json.append(str(path.relative_to(root)))
    return {
        "python_files": checked_python,
        "json_files": checked_json,
    }


def verify_conformance(root: Path, candidate_revision: str) -> dict:
    _require_sha(candidate_revision, "candidate revision")
    engine = _load_module(
        root / "repo/runtime/repo_spec/conformance.py",
        "fs0_build_conformance",
    )
    report = engine.run(root)
    return {
        "candidate_revision": candidate_revision,
        "disposition": report.get("disposition"),
        "failed_assertions": list(report.get("failed_assertions", [])),
        "configuration_errors": list(report.get("configuration_errors", [])),
    }


def collect_assurance_evidence(
    root: Path,
    *,
    stage: str,
    candidate_revision: str,
    work_id: str,
    receipts: list[dict],
) -> dict:
    _require_sha(candidate_revision, "candidate revision")
    assurance = _load_module(
        root / "repo/runtime/repo_spec/assurance.py",
        "fs0_build_assurance",
    )
    required = assurance.obligations_for_stage(root, stage)
    required_ids = {record["id"] for record in required}

    exercised = set()
    validated = []
    for receipt in receipts:
        case = assurance.validate_receipt(
            root,
            receipt,
            candidate_revision=candidate_revision,
            work_id=work_id,
        )
        validated.append(case)
        exercised.update(case["obligation_ids"])

    missing = sorted(required_ids - exercised)
    if missing:
        raise BuildError(f"required Assurance evidence missing: {missing}")
    if any(case["disposition"] != "PASS" for case in validated):
        raise BuildError("acceptance-relevant Assurance receipt is not PASS")

    return {
        "candidate_revision": candidate_revision,
        "work_id": work_id,
        "required_obligation_ids": sorted(required_ids),
        "validated_case_ids": [case["case_id"] for case in validated],
    }


def verify_plan_fidelity(
    context: BuildContext,
    observed_paths: list[str] | tuple[str, ...],
) -> dict:
    reject_mutations_outside_authorized_set(context, observed_paths)
    return {
        "candidate_revision": context.candidate_revision,
        "accepted_plan_id": context.plan_id,
        "authorized_scope_respected": True,
    }


def verify_operational_completion(
    root: Path,
    *,
    candidate_revision: str,
) -> dict:
    _require_sha(candidate_revision, "candidate revision")
    required_surfaces = [
        "README.md",
        "AGENTS.md",
        "LICENSE",
        "repo/authority/requirements.json",
        "repo/authority/framework-contract.json",
        "repo/runtime/repo_spec/design.py",
        "repo/runtime/repo_spec/plan.py",
        "repo/runtime/repo_spec/governance.py",
        "repo/runtime/repo_spec/conformance.py",
        "repo/runtime/repo_spec/assurance.py",
        "repo/runtime/repo_spec/build.py",
        "repo/scripts/validate",
        "repo/state/accepted-state.schema.json",
        "repo/state/state-contract.json",
    ]
    missing = [path for path in required_surfaces if not (root / path).exists()]
    if missing:
        raise BuildError(f"operational completion missing required Genesis surfaces: {missing}")
    return {
        "candidate_revision": candidate_revision,
        "required_surfaces": required_surfaces,
        "operationally_complete": True,
    }


def verify_build(
    root: Path,
    context: BuildContext,
    observed_paths: list[str] | tuple[str, ...],
) -> dict:
    # Build verification establishes syntax, mechanical Conformance, operational
    # completion, and fidelity to the accepted Plan for one exact candidate revision.
    syntax = verify_syntax(root)
    conformance = verify_conformance(root, context.candidate_revision)
    if conformance.get("disposition") != "PASS":
        raise BuildError(
            "Build verification did not establish mechanical Conformance: "
            f"{conformance.get('disposition')}"
        )
    completion = verify_operational_completion(
        root,
        candidate_revision=context.candidate_revision,
    )
    fidelity = verify_plan_fidelity(context, observed_paths)
    return {
        "candidate_revision": context.candidate_revision,
        "accepted_plan_id": context.plan_id,
        "syntax": syntax,
        "conformance": conformance,
        "completion": completion,
        "fidelity": fidelity,
    }
