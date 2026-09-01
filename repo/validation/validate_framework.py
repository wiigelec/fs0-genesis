#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "repo" / "design"
PLANNING = ROOT / "repo" / "planning" / "FS-001-framework-lifecycle-substrate"
FUNCTIONAL_SET = PLANNING / "functional-set.md"
PLAN = PLANNING / "plan.md"
SPEC = ROOT / "repo" / "specs" / "FS-001-framework-lifecycle-substrate.md"
MANIFEST = ROOT / "repo" / "validation" / "requirement-evaluation.json"
ENTRYPOINT = ROOT / "repo" / "scripts" / "validate"
README = ROOT / "README.md"
AGENTS = ROOT / "AGENTS.md"
OLD_WORKFLOW = ROOT / ".github" / "workflows" / "fs0-conformance.yml"
WORKFLOW = ROOT / ".github" / "workflows" / "validation.yml"
EXPECTED_DESIGN_REVISION = "c1012693f67584ec723c572fcce8d4c5ae7e12a8"
TASKS = ("design-corpus", "planning-structure", "manifest-integrity", "validation-entrypoint", "docs-alignment", "ci-delegation", "validation-gate")


def fail(message: str) -> None:
    raise AssertionError(message)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def parse_requirements() -> dict[str, str]:
    text = read(SPEC)
    matches = list(re.finditer(r"^### (FS-001-NR-\d{3}) — .+\n\n\*\*Classification: ([MSB])\*\*$", text, flags=re.MULTILINE))
    result = {m.group(1): m.group(2) for m in matches}
    if len(matches) != 28 or len(result) != 28:
        fail("expected 28 unique FS-001 normative requirements")
    expected = {f"FS-001-NR-{i:03d}" for i in range(1, 29)}
    if set(result) != expected:
        fail("FS-001 requirement identities must be exactly FS-001-NR-001..028")
    return result


def task_design_corpus() -> None:
    if not DESIGN.is_dir():
        fail("repo/design must exist")
    files = [p for p in DESIGN.rglob("*") if p.is_file()]
    if not files:
        fail("repo/design contains no Design documents")
    non_markdown = [str(p.relative_to(ROOT)) for p in files if p.suffix.lower() != ".md"]
    if non_markdown:
        fail(f"canonical Design corpus contains non-Markdown files: {non_markdown}")


def task_planning_structure() -> None:
    for path in (FUNCTIONAL_SET, PLAN):
        if not path.is_file():
            fail(f"missing FS-001 Planning artifact: {path.relative_to(ROOT)}")
    if not SPEC.is_file():
        fail(f"missing FS-001 normative specification: {SPEC.relative_to(ROOT)}")
    fs_text = read(FUNCTIONAL_SET)
    match = re.search(r"^design_revision:\s*([0-9a-f]{40})\s*$", fs_text, flags=re.MULTILINE)
    if not match:
        fail("FS-001 Design revision is missing or not a well-formed 40-character lowercase Git SHA")
    declared_revision = match.group(1)
    cp = subprocess.run(
        ["git", "cat-file", "-e", f"{declared_revision}^{{commit}}"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if cp.returncode != 0:
        fail(f"FS-001 Design revision does not resolve to a Git commit: {declared_revision}")
    if declared_revision != EXPECTED_DESIGN_REVISION or f"`{EXPECTED_DESIGN_REVISION}`" not in fs_text:
        fail("FS-001 does not bind the exact reviewed Design revision")
    parse_requirements()


def load_manifest() -> dict:
    try:
        data = json.loads(read(MANIFEST))
    except json.JSONDecodeError as exc:
        fail(f"invalid Requirement Evaluation Manifest JSON: {exc}")
    if data.get("version") != 1 or not isinstance(data.get("bindings"), list):
        fail("invalid Requirement Evaluation Manifest structure")
    return data


def task_manifest_integrity() -> None:
    requirements = parse_requirements()
    bindings = load_manifest()["bindings"]
    seen = set()
    task_to_requirements = {task: set() for task in TASKS}
    for binding in bindings:
        if not isinstance(binding, dict):
            fail("manifest binding must be an object")
        req = binding.get("requirement")
        tasks = binding.get("tasks")
        if req not in requirements:
            fail(f"manifest references unknown requirement: {req}")
        if req in seen:
            fail(f"duplicate manifest binding for requirement: {req}")
        seen.add(req)
        if not isinstance(tasks, list) or not tasks or len(tasks) != len(set(tasks)):
            fail(f"invalid task list for {req}")
        for task in tasks:
            if task not in TASKS:
                fail(f"manifest references unknown Validation task: {task}")
            task_to_requirements[task].add(req)
    mechanical = {req for req, cls in requirements.items() if cls in {"M", "B"}}
    if seen != mechanical:
        fail(f"manifest binding set mismatch; missing={sorted(mechanical-seen)}, extra={sorted(seen-mechanical)}")
    unbound = sorted(task for task, reqs in task_to_requirements.items() if not reqs)
    if unbound:
        fail(f"Validation tasks without normative justification: {unbound}")


def task_validation_entrypoint() -> None:
    text = read(ENTRYPOINT)
    if not os.access(ENTRYPOINT, os.X_OK):
        fail("repo/scripts/validate must be executable")
    if "repo/validation/validate_framework.py" not in text:
        fail("repo/scripts/validate must delegate to the project-native validator")
    cp = subprocess.run([str(ENTRYPOINT), "--task", "__invalid_required_task__"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode == 0:
        fail("canonical Validation did not fail for an invalid required task")


def task_docs_alignment() -> None:
    readme = read(README)
    agents = read(AGENTS)
    for term in ("Design", "Planning", "Build", "Validation", "Semantic Review", "Acceptance"):
        if term not in readme:
            fail(f"README missing lifecycle term: {term}")
    for value in ("repo/design/", "repo/planning/", "repo/specs/", "repo/scripts/validate", "main"):
        if value not in readme:
            fail(f"README missing active surface: {value}")
    for route in ("→ **Design**", "→ **Planning**", "→ **Build**"):
        if route not in agents:
            fail(f"AGENTS.md missing defect route: {route}")
    if "Do not infer current normative intent from `repo_old/`" not in agents:
        fail("AGENTS.md must deny repo_old normative intent")
    retired = ("canonical mechanical Conformance", "accepted Governance", "Governance acceptance", "FS0 Conformance", "Assurance —", "Conformance —", "Authority —")
    combined = readme + "\n" + agents
    for phrase in retired:
        if phrase in combined:
            fail(f"active documentation retains retired wording: {phrase}")


def task_ci_delegation() -> None:
    if OLD_WORKFLOW.exists():
        fail("retired fs0-conformance workflow remains active")
    text = read(WORKFLOW)
    if "name: Validation" not in text or "run: ./repo/scripts/validate" not in text:
        fail("CI must use Validation terminology and invoke canonical Validation")
    if "repo/validation/validate_framework.py" in text:
        fail("CI must not bypass canonical Validation entry point")
    if "Conformance" in text or "conformance" in text:
        fail("active CI retains retired Conformance terminology")


def aggregate(results: list[bool]) -> bool:
    return all(results)


def task_validation_gate() -> None:
    if set(TASKS) != set(TASK_FUNCTIONS):
        fail("registered Validation task set is incomplete")
    if select_tasks([]) != list(TASKS):
        fail("default canonical Validation must select every registered required task")
    if aggregate([True, True, False]):
        fail("Validation aggregation must fail when a required task fails")
    if not aggregate([True, True, True]):
        fail("Validation aggregation must pass when all required tasks pass")


TASK_FUNCTIONS: dict[str, Callable[[], None]] = {
    "design-corpus": task_design_corpus,
    "planning-structure": task_planning_structure,
    "manifest-integrity": task_manifest_integrity,
    "validation-entrypoint": task_validation_entrypoint,
    "docs-alignment": task_docs_alignment,
    "ci-delegation": task_ci_delegation,
    "validation-gate": task_validation_gate,
}


def select_tasks(argv: list[str]) -> list[str]:
    if argv:
        if len(argv) != 2 or argv[0] != "--task":
            raise ValueError("usage")
        if argv[1] not in TASK_FUNCTIONS:
            raise KeyError(argv[1])
        return [argv[1]]
    return list(TASKS)


def main(argv: list[str]) -> int:
    try:
        selected = select_tasks(argv)
    except ValueError:
        print("usage: repo/scripts/validate [--task TASK]", file=sys.stderr)
        return 2
    except KeyError:
        print(f"unknown Validation task: {argv[1]}", file=sys.stderr)
        return 2
    results = []
    for name in selected:
        try:
            TASK_FUNCTIONS[name]()
        except Exception as exc:
            results.append(False)
            print(f"FAIL {name}: {exc}")
        else:
            results.append(True)
            print(f"PASS {name}")
    return 0 if aggregate(results) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
