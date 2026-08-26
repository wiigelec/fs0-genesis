from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

try:
    from . import design
except ImportError:
    import design  # type: ignore


SHA40_RE = re.compile(r"^[0-9a-f]{40}$")


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

PLAN_ARTIFACT_TYPES = {
    "functional_set": "functional-set",
    "normative_changes": "plan-normative-changes",
    "file_changes": "plan-file-changes",
    "execution": "plan-execution",
    "invariants": "plan-invariants",
    "validation": "plan-validation-intent",
    "assurance": "plan-assurance-intent",
    "completion": "plan-completion",
}


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

    if root.get("schema_version") != "1":
        raise PlanError("plan.json schema_version must be 1")
    if root.get("artifact_type") != "plan":
        raise PlanError("plan.json artifact_type must be plan")
    plan_id = root.get("plan_id")
    status = root.get("status")
    purpose = root.get("purpose")
    if not isinstance(plan_id, str) or not plan_id:
        raise PlanError("plan.json requires stable plan_id")
    if not isinstance(status, str) or not status:
        raise PlanError("plan.json requires status")
    if not isinstance(purpose, str) or not purpose:
        raise PlanError("plan.json requires purpose")

    documents: dict[str, dict] = {}
    for key in PLAN_REFERENCES:
        relative = root.get(key)
        if not isinstance(relative, str) or not relative:
            raise PlanError(f"plan.json missing document reference: {key}")
        document = _load_json(_safe_child(directory, relative))
        if document.get("schema_version") != "1":
            raise PlanError(f"{key} schema_version must be 1")
        expected_type = PLAN_ARTIFACT_TYPES[key]
        if document.get("artifact_type") != expected_type:
            raise PlanError(f"{key} artifact_type must be {expected_type}: {document.get('artifact_type')}")
        if key != "functional_set" and document.get("plan_id") != plan_id:
            raise PlanError(f"{key} plan_id must match root plan_id")
        documents[key] = document

    return LoadedPlan(directory=directory, root=root, documents=documents)


def validate_functional_set_structure(plan: LoadedPlan) -> None:
    fs = plan.functional_set
    if "accepted_predecessor" not in fs:
        raise PlanError("functional-set.json requires accepted_predecessor field")
    identity = fs.get("functional_set")
    if not isinstance(identity, dict):
        raise PlanError("functional-set.json requires functional_set object")
    order = identity.get("order")
    if type(order) is not int or order < 0:
        raise PlanError("functional_set.order must be a non-negative integer")
    for key in ("id", "kind", "title", "description"):
        value = identity.get(key)
        if not isinstance(value, str) or not value:
            raise PlanError(f"functional_set.{key} must be a non-empty string")


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

    if not isinstance(predecessor, dict):
        raise PlanError(
            "non-Genesis accepted predecessor must be an object identifying accepted_revision"
        )

    accepted_revision = predecessor.get("accepted_revision")
    if not isinstance(accepted_revision, str) or not SHA40_RE.fullmatch(accepted_revision):
        raise PlanError(
            "non-Genesis accepted predecessor accepted_revision must be exact 40-hex repository revision"
        )


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


def validate_normative_changes(plan: LoadedPlan) -> None:
    document = plan.documents["normative_changes"]
    changes = document.get("changes")
    if not isinstance(changes, list):
        raise PlanError("normative-changes document requires changes list")
    seen: set[str] = set()
    for change in changes:
        if not isinstance(change, dict):
            raise PlanError("normative change must be object")
        operation = change.get("operation")
        requirement = change.get("requirement")
        if not isinstance(operation, str) or not operation:
            raise PlanError("normative change requires operation")
        if not isinstance(requirement, dict):
            raise PlanError("normative change requires requirement object")
        rid = requirement.get("id")
        statement = requirement.get("statement")
        lifecycle = requirement.get("lifecycle")
        evaluation = requirement.get("evaluation")
        if not all(isinstance(value, str) and value for value in (rid, statement, lifecycle)):
            raise PlanError("normative requirement requires id, statement, and lifecycle")
        if rid in seen:
            raise PlanError(f"duplicate normative requirement identity: {rid}")
        seen.add(rid)
        if not isinstance(evaluation, dict):
            raise PlanError(f"{rid} requires evaluation")
        conf = evaluation.get("conformance")
        assur = evaluation.get("assurance")
        if not isinstance(conf, dict) or not isinstance(assur, dict):
            raise PlanError(f"{rid} requires Conformance and Assurance evaluation")
        if conf.get("applicability") not in {"mechanical", "none"}:
            raise PlanError(f"{rid} has invalid Conformance applicability")
        if assur.get("applicability") not in {"required", "none"}:
            raise PlanError(f"{rid} has invalid Assurance applicability")


def validate_intent_documents(plan: LoadedPlan) -> None:
    for key in ("invariants", "validation", "assurance", "completion"):
        if not isinstance(plan.documents[key], dict):
            raise PlanError(f"{key} document must be object")


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
        requirement_ids = change.get("requirement_ids")
        purpose = change.get("purpose")
        implementation = change.get("implementation")
        if not isinstance(requirement_ids, list) or not all(isinstance(item, str) and item for item in requirement_ids) or len(requirement_ids) != len(set(requirement_ids)):
            raise PlanError(f"{cid} requires unique requirement_ids string list")
        if not isinstance(purpose, str) or not purpose:
            raise PlanError(f"{cid} requires purpose")
        if not isinstance(implementation, list) or not all(isinstance(item, str) and item for item in implementation):
            raise PlanError(f"{cid} requires implementation string list")
        dependencies = change.get("dependencies")
        if dependencies is not None:
            if not isinstance(dependencies, list) or not all(isinstance(item, str) and item for item in dependencies) or len(dependencies) != len(set(dependencies)):
                raise PlanError(f"{cid} dependencies must be unique string list")
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
        stage_id = stage.get("id")
        if not isinstance(order, int) or order < 1 or order in orders:
            raise PlanError(f"invalid or duplicate execution order: {order}")
        if not isinstance(stage_id, str) or not stage_id:
            raise PlanError("execution stage requires id")
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
    validate_functional_set_structure(plan)
    validate_predecessor_rules(plan)
    validate_design_scope(root, plan)
    validate_normative_changes(plan)
    file_changes(plan)
    validate_execution_references(plan)
    validate_intent_documents(plan)
    return plan
