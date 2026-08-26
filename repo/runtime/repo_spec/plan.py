from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

try:
    from . import design
except ImportError:
    import design  # type: ignore


class PlanError(ValueError):
    pass


PLAN_REFERENCES = (
    "functional_set",
    "normative_changes",
    "file_changes",
    "execution",
    "invariants",
    "validation",
    "assurance",
    "completion",
)


@dataclass(frozen=True)
class LoadedPlan:
    directory: Path
    root: dict
    documents: dict[str, dict]

    @property
    def functional_set(self) -> dict:
        return self.documents["functional_set"]

    @property
    def file_changes(self) -> dict:
        return self.documents["file_changes"]


def _load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PlanError(f"unable to load Plan artifact {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PlanError(f"Plan artifact must be an object: {path}")
    return value


def _safe_child(directory: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise PlanError("Plan document reference must be a non-empty string")
    path = (directory / relative).resolve()
    try:
        path.relative_to(directory.resolve())
    except ValueError as exc:
        raise PlanError(f"Plan reference escapes functional-set directory: {relative}") from exc
    return path


def load_plan(plan_directory: Path) -> LoadedPlan:
    directory = plan_directory.resolve()
    root_path = directory / "plan.json"
    root = _load_json(root_path)

    if root.get("artifact_type") != "plan":
        raise PlanError("plan.json artifact_type must be plan")

    documents: dict[str, dict] = {}
    for key in PLAN_REFERENCES:
        relative = root.get(key)
        if not isinstance(relative, str) or not relative:
            raise PlanError(f"plan.json missing document reference: {key}")
        documents[key] = _load_json(_safe_child(directory, relative))

    return LoadedPlan(directory=directory, root=root, documents=documents)


def validate_predecessor_rules(plan: LoadedPlan) -> None:
    fs = plan.functional_set
    identity = fs.get("functional_set")
    if not isinstance(identity, dict):
        raise PlanError("functional-set.json requires functional_set object")

    fs_id = identity.get("id")
    kind = identity.get("kind")
    predecessor = fs.get("accepted_predecessor")

    if fs_id == "FS0-GENESIS":
        if kind != "genesis":
            raise PlanError("FS0-GENESIS must have kind genesis")
        if predecessor is not None:
            raise PlanError("FS0-GENESIS must not have an accepted predecessor")
        return

    if predecessor is None:
        raise PlanError("non-Genesis functional set requires an accepted predecessor")

    if isinstance(predecessor, str):
        if not predecessor:
            raise PlanError("accepted predecessor string must be non-empty")
        return

    if isinstance(predecessor, dict):
        if not predecessor:
            raise PlanError("accepted predecessor object must not be empty")
        return

    raise PlanError("accepted predecessor must be string, object, or null for Genesis")


def validate_design_scope(root: Path, plan: LoadedPlan) -> None:
    fs = plan.functional_set
    inputs = fs.get("design_inputs")
    if not isinstance(inputs, list) or not inputs:
        raise PlanError("functional set requires Design inputs")

    for design_input in inputs:
        if not isinstance(design_input, dict):
            raise PlanError("Design input must be an object")
        try:
            design.resolve_selected_statements(root, design_input)
        except design.DesignError as exc:
            raise PlanError(str(exc)) from exc


def file_changes(plan: LoadedPlan) -> tuple[dict, ...]:
    changes = plan.file_changes.get("changes")
    if not isinstance(changes, list):
        raise PlanError("file-changes document requires changes list")

    seen_ids: set[str] = set()
    observed: list[dict] = []
    for change in changes:
        if not isinstance(change, dict):
            raise PlanError("file change must be object")
        cid = change.get("id")
        path = change.get("path")
        operation = change.get("operation")
        if not isinstance(cid, str) or not cid:
            raise PlanError("file change requires stable id")
        if cid in seen_ids:
            raise PlanError(f"duplicate file-change id: {cid}")
        seen_ids.add(cid)
        if not isinstance(path, str) or not path:
            raise PlanError(f"{cid} requires path")
        if not isinstance(operation, str) or not operation:
            raise PlanError(f"{cid} requires explicit operation")
        observed.append(change)
    return tuple(observed)


def authorized_mutation_set(plan: LoadedPlan) -> tuple[str, ...]:
    paths: list[str] = []
    for change in file_changes(plan):
        path = change["path"]
        if path not in paths:
            paths.append(path)
    return tuple(paths)


def validate_execution_references(plan: LoadedPlan) -> None:
    known = {change["id"] for change in file_changes(plan)}
    execution = plan.documents["execution"]
    stages = execution.get("stages")
    if not isinstance(stages, list) or not stages:
        raise PlanError("execution document requires stages")

    referenced: set[str] = set()
    orders: set[int] = set()
    for stage in stages:
        if not isinstance(stage, dict):
            raise PlanError("execution stage must be object")
        order = stage.get("order")
        if not isinstance(order, int) or order < 1 or order in orders:
            raise PlanError(f"invalid or duplicate execution order: {order}")
        orders.add(order)
        ids = stage.get("file_change_ids", [])
        if not isinstance(ids, list) or not all(isinstance(x, str) and x for x in ids):
            raise PlanError("execution file_change_ids must be string list")
        for cid in ids:
            if cid not in known:
                raise PlanError(f"execution references unknown file change: {cid}")
            if cid in referenced:
                raise PlanError(f"file change appears in multiple execution stages: {cid}")
            referenced.add(cid)

    missing = known - referenced
    if missing:
        raise PlanError(f"planned file changes unreachable from execution sequencing: {sorted(missing)}")


def validate_plan(root: Path, plan_directory: Path) -> LoadedPlan:
    plan = load_plan(plan_directory)
    validate_predecessor_rules(plan)
    validate_design_scope(root, plan)
    file_changes(plan)
    validate_execution_references(plan)
    return plan
