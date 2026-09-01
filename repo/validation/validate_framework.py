#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "repo" / "design"
PLANNING_ROOT = ROOT / "repo" / "planning"
SPECS_ROOT = ROOT / "repo" / "specs"
MANIFEST = ROOT / "repo" / "validation" / "requirement-evaluation.json"
ENTRYPOINT = ROOT / "repo" / "scripts" / "validate"
README = ROOT / "README.md"
AGENTS = ROOT / "AGENTS.md"
OLD_WORKFLOW = ROOT / ".github" / "workflows" / "fs0-conformance.yml"
WORKFLOW = ROOT / ".github" / "workflows" / "validation.yml"

TASKS = (
    "design-corpus",
    "planning-structure",
    "manifest-integrity",
    "validation-entrypoint",
    "docs-alignment",
    "ci-delegation",
    "validation-gate",
    "framework-regression",
)

FS_BASENAME_RE = re.compile(r"^(FS-\d{3})-(.+)$")
REQ_HEADING_RE = re.compile(r"^### (FS-\d{3}-NR-\d{3}) — .+$", re.MULTILINE)
ALL_H3_RE = re.compile(r"^### (.+)$", re.MULTILINE)

# FS-001 has an explicit mechanical requirement naming the exact Design revision.
FS001_DESIGN_REVISION = "c1012693f67584ec723c572fcce8d4c5ae7e12a8"


def fail(message: str) -> None:
    raise AssertionError(message)


def read(path: Path) -> str:
    if not path.is_file():
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            rel = path
        fail(f"missing file: {rel}")
    return path.read_text(encoding="utf-8")


def git_commit_exists(revision: str) -> bool:
    cp = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}^{{commit}}"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return cp.returncode == 0


def discover_functional_sets(
    planning_root: Path = PLANNING_ROOT,
    specs_root: Path = SPECS_ROOT,
) -> list[tuple[str, str, Path, Path]]:
    planning: dict[str, tuple[str, Path]] = {}
    specs: dict[str, tuple[str, Path]] = {}

    if not planning_root.is_dir():
        fail("repo/planning must exist")
    if not specs_root.is_dir():
        fail("repo/specs must exist")

    for path in planning_root.iterdir():
        if not path.is_dir() or not path.name.startswith("FS-"):
            continue
        match = FS_BASENAME_RE.fullmatch(path.name)
        if not match:
            fail(f"invalid Functional Set Planning directory name: {path.name}")
        fs_id = match.group(1)
        if fs_id in planning:
            fail(f"duplicate Functional Set Planning identity: {fs_id}")
        planning[fs_id] = (path.name, path)

    for path in specs_root.iterdir():
        if not path.is_file() or path.suffix != ".md" or not path.name.startswith("FS-"):
            continue
        match = FS_BASENAME_RE.fullmatch(path.stem)
        if not match:
            fail(f"invalid Functional Set specification name: {path.name}")
        fs_id = match.group(1)
        if fs_id in specs:
            fail(f"duplicate Functional Set specification identity: {fs_id}")
        specs[fs_id] = (path.stem, path)

    if set(planning) != set(specs):
        fail(
            "Functional Set Planning/specification correspondence mismatch; "
            f"planning_only={sorted(set(planning)-set(specs))}, "
            f"spec_only={sorted(set(specs)-set(planning))}"
        )

    result = []
    for fs_id in sorted(planning):
        planning_name, planning_dir = planning[fs_id]
        spec_name, spec_path = specs[fs_id]
        if planning_name != spec_name:
            fail(
                f"Functional Set Planning/specification basename mismatch for {fs_id}: "
                f"{planning_name} != {spec_name}"
            )
        result.append((fs_id, planning_name, planning_dir, spec_path))
    return result


def parse_specification(spec_path: Path, fs_id: str) -> tuple[dict[str, str], set[str]]:
    text = read(spec_path)
    title = re.search(r"^# (FS-\d{3})\b", text, flags=re.MULTILINE)
    if not title or title.group(1) != fs_id:
        fail(f"{spec_path.name} specification identity does not match {fs_id}")

    all_h3 = ALL_H3_RE.findall(text)
    headings = list(REQ_HEADING_RE.finditer(text))
    if len(all_h3) != len(headings):
        malformed = [
            heading
            for heading in all_h3
            if not re.fullmatch(r"FS-\d{3}-NR-\d{3} — .+", heading)
        ]
        fail(f"{spec_path.name} contains malformed normative requirement heading: {malformed}")

    requirements: dict[str, str] = {}
    inactive: set[str] = set()

    for index, heading_match in enumerate(headings):
        req = heading_match.group(1)
        if not req.startswith(fs_id + "-NR-"):
            fail(f"{spec_path.name} requirement identity does not match owning Functional Set: {req}")
        if req in requirements:
            fail(f"duplicate normative requirement identity: {req}")

        block_end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        block = text[heading_match.end():block_end]

        classifications = re.findall(
            r"^\*\*Classification: ([^*\n]+)\*\*$",
            block,
            flags=re.MULTILINE,
        )
        if len(classifications) != 1 or classifications[0] not in {"M", "S", "B"}:
            fail(
                f"{spec_path.name} requirement {req} must contain exactly one "
                "Classification of M, S, or B"
            )

        states = re.findall(
            r"^\*\*State: ([^*\n]+)\*\*$",
            block,
            flags=re.MULTILINE,
        )
        if len(states) > 1:
            fail(f"{spec_path.name} requirement {req} contains duplicate State markers")
        if states and states[0] != "Inactive":
            fail(
                f"{spec_path.name} requirement {req} State must be Inactive "
                "when explicitly present"
            )

        requirements[req] = classifications[0]
        if states:
            inactive.add(req)

    if not requirements:
        fail(f"{spec_path.name} contains no normative requirements")
    return requirements, inactive

def validate_functional_set(
    fs_id: str,
    planning_dir: Path,
    spec_path: Path,
) -> tuple[dict[str, str], set[str]]:
    functional_set = planning_dir / "functional-set.md"
    plan = planning_dir / "plan.md"
    for path in (functional_set, plan):
        if not path.is_file():
            fail(f"missing {fs_id} Planning artifact: {path.name}")

    fs_text = read(functional_set)
    id_matches = re.findall(
        r"^functional_set:\s*(FS-\d{3})\s*$",
        fs_text,
        flags=re.MULTILINE,
    )
    if len(id_matches) != 1 or id_matches[0] != fs_id:
        fail(
            f"{fs_id} functional-set.md identity mismatch: "
            "expected exactly one matching functional_set identity"
        )

    revision_matches = re.findall(
        r"^design_revision:\s*([^\s]+)\s*$",
        fs_text,
        flags=re.MULTILINE,
    )
    if len(revision_matches) != 1 or not re.fullmatch(r"[0-9a-f]{40}", revision_matches[0]):
        fail(
            f"{fs_id} must contain exactly one well-formed "
            "40-character lowercase Git design_revision"
        )
    revision = revision_matches[0]
    if not git_commit_exists(revision):
        fail(f"{fs_id} Design revision does not resolve to a Git commit: {revision}")

    if fs_id == "FS-001" and revision != FS001_DESIGN_REVISION:
        fail("FS-001 does not identify its exact normative Design revision")

    return parse_specification(spec_path, fs_id)

def collect_requirement_state(
    planning_root: Path = PLANNING_ROOT,
    specs_root: Path = SPECS_ROOT,
) -> tuple[dict[str, str], set[str]]:
    requirements: dict[str, str] = {}
    inactive: set[str] = set()
    for fs_id, _, planning_dir, spec_path in discover_functional_sets(planning_root, specs_root):
        parsed, parsed_inactive = validate_functional_set(fs_id, planning_dir, spec_path)
        overlap = set(requirements) & set(parsed)
        if overlap:
            fail(f"duplicate normative requirement identities across specifications: {sorted(overlap)}")
        requirements.update(parsed)
        inactive.update(parsed_inactive)
    return requirements, inactive


def collect_requirements(
    planning_root: Path = PLANNING_ROOT,
    specs_root: Path = SPECS_ROOT,
) -> dict[str, str]:
    requirements, _ = collect_requirement_state(planning_root, specs_root)
    return requirements


def load_manifest(path: Path = MANIFEST) -> dict:
    try:
        data = json.loads(read(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid Requirement Evaluation Manifest JSON: {exc}")
    if data.get("version") != 1 or not isinstance(data.get("bindings"), list):
        fail("invalid Requirement Evaluation Manifest structure")
    return data


def validate_manifest_data(
    requirements: dict[str, str],
    data: dict,
    tasks: tuple[str, ...] = TASKS,
    required_bindings: set[str] | None = None,
    forbidden_bindings: set[str] | None = None,
) -> None:
    bindings = data["bindings"]
    seen: set[str] = set()
    task_to_requirements = {task: set() for task in tasks}

    for binding in bindings:
        if not isinstance(binding, dict):
            fail("manifest binding must be an object")
        req = binding.get("requirement")
        bound_tasks = binding.get("tasks")
        if req not in requirements:
            fail(f"manifest references unknown requirement: {req}")
        if requirements[req] not in {"M", "B"}:
            fail(f"manifest references requirement without active mechanical evaluation: {req}")
        if req in seen:
            fail(f"duplicate manifest binding for requirement: {req}")
        seen.add(req)
        if (
            not isinstance(bound_tasks, list)
            or not bound_tasks
            or len(bound_tasks) != len(set(bound_tasks))
        ):
            fail(f"invalid task list for {req}")
        for task in bound_tasks:
            if task not in tasks:
                fail(f"manifest references unknown Validation task: {task}")
            task_to_requirements[task].add(req)

    if required_bindings is not None:
        missing = sorted(required_bindings - seen)
        if missing:
            fail(f"active mechanically evaluated requirements without manifest bindings: {missing}")

    if forbidden_bindings is not None:
        forbidden = sorted(forbidden_bindings & seen)
        if forbidden:
            fail(f"inactive requirements must not have manifest bindings: {forbidden}")

    unjustified = sorted(task for task, reqs in task_to_requirements.items() if not reqs)
    if unjustified:
        fail(f"Validation tasks without current normative justification: {unjustified}")


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
    collect_requirements()


def task_manifest_integrity() -> None:
    requirements, inactive = collect_requirement_state()
    required_bindings = {
        req
        for req, classification in requirements.items()
        if classification in {"M", "B"} and req not in inactive
    }
    validate_manifest_data(
        requirements,
        load_manifest(),
        required_bindings=required_bindings,
        forbidden_bindings=inactive,
    )


def task_validation_entrypoint() -> None:
    text = read(ENTRYPOINT)
    if not os.access(ENTRYPOINT, os.X_OK):
        fail("repo/scripts/validate must be executable")
    if "repo/validation/validate_framework.py" not in text:
        fail("repo/scripts/validate must delegate to the project-native validator")
    cp = subprocess.run(
        [str(ENTRYPOINT), "--task", "__invalid_required_task__"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
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
    retired = (
        "canonical mechanical Conformance",
        "accepted Governance",
        "Governance acceptance",
        "FS0 Conformance",
        "Assurance —",
        "Conformance —",
        "Authority —",
    )
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


def write_fixture_fs(
    planning_root: Path,
    specs_root: Path,
    basename: str,
    fs_id: str,
    revision: str,
    requirement_id: str,
    classification: str,
) -> None:
    planning_dir = planning_root / basename
    planning_dir.mkdir(parents=True)
    (planning_dir / "functional-set.md").write_text(
        f"---\nfunctional_set: {fs_id}\ntitle: Fixture\ndesign_revision: {revision}\n---\n",
        encoding="utf-8",
    )
    (planning_dir / "plan.md").write_text("# Fixture Plan\n", encoding="utf-8")
    (specs_root / f"{basename}.md").write_text(
        f"# {fs_id} — Fixture\n\n"
        f"### {requirement_id} — Fixture requirement\n\n"
        f"**Classification: {classification}**\n\nFixture obligation.\n",
        encoding="utf-8",
    )


def expect_failure(fn: Callable[[], object], contains: str) -> None:
    try:
        fn()
    except Exception as exc:
        if contains not in str(exc):
            fail(f"regression expected diagnostic containing {contains!r}, observed: {exc}")
    else:
        fail(f"regression expected failure containing {contains!r}")


def task_framework_regression() -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.strip()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        planning = root / "planning"
        specs = root / "specs"
        planning.mkdir()
        specs.mkdir()

        write_fixture_fs(
            planning,
            specs,
            "FS-998-fixture",
            "FS-998",
            head,
            "FS-998-NR-001",
            "S",
        )
        reqs = collect_requirements(planning, specs)
        if reqs != {"FS-998-NR-001": "S"}:
            fail("generic later Functional Set discovery/parsing regression failed")

        (specs / "FS-998-fixture.md").unlink()
        expect_failure(
            lambda: collect_requirements(planning, specs),
            "correspondence mismatch",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        planning = root / "planning"
        specs = root / "specs"
        planning.mkdir()
        specs.mkdir()

        write_fixture_fs(
            planning,
            specs,
            "FS-998-fixture",
            "FS-998",
            "0" * 40,
            "FS-998-NR-001",
            "M",
        )
        expect_failure(
            lambda: collect_requirements(planning, specs),
            "does not resolve to a Git commit",
        )

        fs_path = planning / "FS-998-fixture" / "functional-set.md"
        text = fs_path.read_text(encoding="utf-8").replace(
            "functional_set: FS-998",
            "functional_set: FS-997",
        )
        fs_path.write_text(text.replace("0" * 40, head), encoding="utf-8")
        expect_failure(
            lambda: collect_requirements(planning, specs),
            "identity mismatch",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        planning = root / "planning"
        specs = root / "specs"
        planning.mkdir()
        specs.mkdir()

        write_fixture_fs(
            planning, specs, "FS-998-fixture", "FS-998", head,
            "FS-997-NR-001", "M",
        )
        expect_failure(
            lambda: collect_requirements(planning, specs),
            "requirement identity does not match owning Functional Set",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        planning = root / "planning"
        specs = root / "specs"
        planning.mkdir()
        specs.mkdir()

        write_fixture_fs(
            planning, specs, "FS-998-fixture", "FS-998", head,
            "FS-998-NR-001", "M",
        )
        spec_path = specs / "FS-998-fixture.md"
        spec_text = spec_path.read_text(encoding="utf-8")
        spec_path.write_text(
            spec_text.replace("**Classification: M**", "**Classification: X**"),
            encoding="utf-8",
        )
        expect_failure(
            lambda: collect_requirements(planning, specs),
            "Classification of M, S, or B",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        planning = root / "planning"
        specs = root / "specs"
        planning.mkdir()
        specs.mkdir()

        write_fixture_fs(
            planning, specs, "FS-998-fixture", "FS-998", head,
            "FS-998-NR-001", "M",
        )
        spec_path = specs / "FS-998-fixture.md"
        with spec_path.open("a", encoding="utf-8") as handle:
            handle.write(
                "\n### FS-998-NR-001 — Duplicate fixture requirement\n\n"
                "**Classification: M**\n\nDuplicate obligation.\n"
            )
        expect_failure(
            lambda: collect_requirements(planning, specs),
            "duplicate normative requirement identity",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        planning = root / "planning"
        specs = root / "specs"
        planning.mkdir()
        specs.mkdir()

        write_fixture_fs(
            planning, specs, "FS-998-Fixture_Name", "FS-998", head,
            "FS-998-NR-001", "M",
        )
        reqs = collect_requirements(planning, specs)
        if reqs != {"FS-998-NR-001": "M"}:
            fail("descriptive Functional Set suffix must not create a second identity grammar")

        spec_path = specs / "FS-998-Fixture_Name.md"
        base_spec = spec_path.read_text(encoding="utf-8")
        for malformed_heading in (
            "FS-998-NR-01 — Malformed requirement",
            "FS-998-NR001 — Malformed requirement",
            "FS998-NR-001 — Malformed requirement",
            "FS-998-REQ-001 — Malformed requirement",
        ):
            spec_path.write_text(
                base_spec
                + f"\n### {malformed_heading}\n\n"
                + "**Classification: M**\n\nMalformed.\n",
                encoding="utf-8",
            )
            expect_failure(
                lambda: collect_requirements(planning, specs),
                "malformed normative requirement heading",
            )

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        planning = root / "planning"
        specs = root / "specs"
        planning.mkdir()
        specs.mkdir()

        write_fixture_fs(
            planning, specs, "FS-998-fixture", "FS-998", head,
            "FS-998-NR-001", "M",
        )
        spec_path = specs / "FS-998-fixture.md"
        spec_text = spec_path.read_text(encoding="utf-8")
        spec_path.write_text(
            spec_text.replace(
                "**Classification: M**\n\nFixture obligation.",
                "**Classification: M**\n\n**Classification: S**\n\nFixture obligation.",
            ),
            encoding="utf-8",
        )
        expect_failure(
            lambda: collect_requirements(planning, specs),
            "exactly one Classification",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        planning = root / "planning"
        specs = root / "specs"
        planning.mkdir()
        specs.mkdir()

        write_fixture_fs(
            planning, specs, "FS-998-fixture", "FS-998", head,
            "FS-998-NR-001", "M",
        )
        fs_path = planning / "FS-998-fixture" / "functional-set.md"
        fs_text = fs_path.read_text(encoding="utf-8")
        fs_path.write_text(
            fs_text.replace(
                "functional_set: FS-998",
                "functional_set: FS-998\nfunctional_set: FS-998",
            ),
            encoding="utf-8",
        )
        expect_failure(
            lambda: collect_requirements(planning, specs),
            "exactly one matching functional_set",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        planning = root / "planning"
        specs = root / "specs"
        planning.mkdir()
        specs.mkdir()

        write_fixture_fs(
            planning, specs, "FS-998-fixture", "FS-998", head,
            "FS-998-NR-001", "M",
        )
        fs_path = planning / "FS-998-fixture" / "functional-set.md"
        fs_text = fs_path.read_text(encoding="utf-8")
        fs_path.write_text(
            fs_text.replace(
                f"design_revision: {head}",
                f"design_revision: {head}\ndesign_revision: {head}",
            ),
            encoding="utf-8",
        )
        expect_failure(
            lambda: collect_requirements(planning, specs),
            "exactly one well-formed",
        )

    # Retired I evaluation classification is invalid.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        planning = root / "planning"
        specs = root / "specs"
        planning.mkdir()
        specs.mkdir()

        write_fixture_fs(
            planning, specs, "FS-998-fixture", "FS-998", head,
            "FS-998-NR-001", "I",
        )
        expect_failure(
            lambda: collect_requirement_state(planning, specs),
            "Classification of M, S, or B",
        )

    # Requirement state is separate from evaluation classification.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        planning = root / "planning"
        specs = root / "specs"
        planning.mkdir()
        specs.mkdir()

        write_fixture_fs(
            planning, specs, "FS-998-fixture", "FS-998", head,
            "FS-998-NR-001", "M",
        )
        spec_path = specs / "FS-998-fixture.md"
        active_text = spec_path.read_text(encoding="utf-8")
        inactive_text = active_text.replace(
            "**Classification: M**",
            "**Classification: M**\n\n**State: Inactive**",
            1,
        )
        spec_path.write_text(inactive_text, encoding="utf-8")

        fixture_requirements, fixture_inactive = collect_requirement_state(
            planning, specs
        )
        if fixture_requirements != {"FS-998-NR-001": "M"}:
            fail("inactive requirement must retain its evaluation classification")
        if fixture_inactive != {"FS-998-NR-001"}:
            fail("inactive requirement state was not parsed")

        validate_manifest_data(
            fixture_requirements,
            {"version": 1, "bindings": []},
            tasks=(),
            required_bindings=set(),
            forbidden_bindings=fixture_inactive,
        )
        expect_failure(
            lambda: validate_manifest_data(
                fixture_requirements,
                {
                    "version": 1,
                    "bindings": [
                        {
                            "requirement": "FS-998-NR-001",
                            "tasks": ["planning-structure"],
                        }
                    ],
                },
                tasks=("planning-structure",),
                required_bindings=set(),
                forbidden_bindings=fixture_inactive,
            ),
            "inactive requirements must not have manifest bindings",
        )

        spec_path.write_text(active_text, encoding="utf-8")
        reactivated, reactivated_inactive = collect_requirement_state(
            planning, specs
        )
        if reactivated != {"FS-998-NR-001": "M"} or reactivated_inactive:
            fail("reactivation by removing State: Inactive failed")

    for state_marker, diagnostic in (
        ("**State: Active**", "State must be Inactive"),
        (
            "**State: Inactive**\n\n**State: Inactive**",
            "duplicate State markers",
        ),
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planning = root / "planning"
            specs = root / "specs"
            planning.mkdir()
            specs.mkdir()

            write_fixture_fs(
                planning, specs, "FS-998-fixture", "FS-998", head,
                "FS-998-NR-001", "M",
            )
            spec_path = specs / "FS-998-fixture.md"
            fixture_text = spec_path.read_text(encoding="utf-8")
            spec_path.write_text(
                fixture_text.replace(
                    "**Classification: M**",
                    "**Classification: M**\n\n" + state_marker,
                    1,
                ),
                encoding="utf-8",
            )
            expect_failure(
                lambda: collect_requirement_state(planning, specs),
                diagnostic,
            )

    requirements = {
        "FS-998-NR-001": "M",
        "FS-998-NR-002": "S",
    }
    expect_failure(
        lambda: validate_manifest_data(
            requirements,
            {"version": 1, "bindings": []},
            tasks=(),
            required_bindings={"FS-998-NR-001"},
        ),
        "without manifest bindings",
    )
    expect_failure(
        lambda: validate_manifest_data(
            requirements,
            {"version": 1, "bindings": [{"requirement": "FS-998-NR-999", "tasks": ["planning-structure"]}]},
        ),
        "unknown requirement",
    )
    expect_failure(
        lambda: validate_manifest_data(
            requirements,
            {"version": 1, "bindings": [{"requirement": "FS-998-NR-002", "tasks": ["planning-structure"]}]},
        ),
        "without active mechanical evaluation",
    )
    expect_failure(
        lambda: validate_manifest_data(
            requirements,
            {"version": 1, "bindings": [{"requirement": "FS-998-NR-001", "tasks": ["missing-task"]}]},
        ),
        "unknown Validation task",
    )

    all_current = {
        "FS-997-NR-001": "M",
        "FS-998-NR-001": "M",
    }
    expect_failure(
        lambda: validate_manifest_data(
            all_current,
            {
                "version": 1,
                "bindings": [
                    {"requirement": "FS-998-NR-001", "tasks": ["planning-structure"]}
                ],
            },
            tasks=("planning-structure",),
            required_bindings=set(all_current),
        ),
        "without manifest bindings",
    )

TASK_FUNCTIONS: dict[str, Callable[[], None]] = {
    "design-corpus": task_design_corpus,
    "planning-structure": task_planning_structure,
    "manifest-integrity": task_manifest_integrity,
    "validation-entrypoint": task_validation_entrypoint,
    "docs-alignment": task_docs_alignment,
    "ci-delegation": task_ci_delegation,
    "validation-gate": task_validation_gate,
    "framework-regression": task_framework_regression,
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
