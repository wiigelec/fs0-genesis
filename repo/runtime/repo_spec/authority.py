from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


class AuthorityError(ValueError):
    pass


@dataclass(frozen=True)
class Requirement:
    id: str
    statement: str
    lifecycle: str
    conformance_applicability: str
    assurance_applicability: str


def _load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuthorityError(f"unable to load authority artifact {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AuthorityError(f"authority artifact must be object: {path}")
    return value


def load_requirements(root: Path) -> dict[str, Requirement]:
    data = _load_json(root / "repo/authority/requirements.json")
    records = data.get("requirements")
    if not isinstance(records, list):
        raise AuthorityError("requirements registry requires requirements list")

    resolved: dict[str, Requirement] = {}
    for record in records:
        if not isinstance(record, dict):
            raise AuthorityError("requirement record must be object")
        rid = record.get("id")
        statement = record.get("statement")
        lifecycle = record.get("lifecycle")
        evaluation = record.get("evaluation")
        if not all(isinstance(x, str) and x for x in (rid, statement, lifecycle)):
            raise AuthorityError("requirement requires id, statement, and lifecycle")
        if rid in resolved:
            raise AuthorityError(f"duplicate requirement ID: {rid}")
        if not isinstance(evaluation, dict):
            raise AuthorityError(f"{rid} requires evaluation")
        conf = evaluation.get("conformance")
        assur = evaluation.get("assurance")
        if not isinstance(conf, dict) or not isinstance(assur, dict):
            raise AuthorityError(f"{rid} requires Conformance and Assurance evaluation")
        conf_app = conf.get("applicability")
        assur_app = assur.get("applicability")
        if conf_app not in {"mechanical", "none"}:
            raise AuthorityError(f"{rid} malformed Conformance applicability: {conf_app}")
        if assur_app not in {"required", "none"}:
            raise AuthorityError(f"{rid} malformed Assurance applicability: {assur_app}")
        resolved[rid] = Requirement(
            id=rid,
            statement=statement,
            lifecycle=lifecycle,
            conformance_applicability=conf_app,
            assurance_applicability=assur_app,
        )
    return resolved


def load_framework_contract(root: Path) -> dict:
    data = _load_json(root / "repo/authority/framework-contract.json")
    if data.get("authority_namespace") != "repo/":
        raise AuthorityError("framework authority namespace must be repo/")
    keystones = data.get("keystones")
    if not isinstance(keystones, list):
        raise AuthorityError("framework contract requires keystones")
    ids = [k.get("id") for k in keystones if isinstance(k, dict)]
    if ids != ["Governance", "Conformance", "Assurance"]:
        raise AuthorityError(
            "framework contract must declare exactly Governance, Conformance, Assurance"
        )
    if len(ids) != 3 or len(set(ids)) != 3:
        raise AuthorityError("framework contract keystone identity defect")
    return data


def requirement(root: Path, requirement_id: str) -> Requirement:
    try:
        return load_requirements(root)[requirement_id]
    except KeyError as exc:
        raise AuthorityError(f"unknown accepted requirement: {requirement_id}") from exc


def delegated_keystone(root: Path, keystone_id: str) -> dict:
    contract = load_framework_contract(root)
    for keystone in contract["keystones"]:
        if keystone["id"] == keystone_id:
            return dict(keystone)
    raise AuthorityError(f"unknown authority keystone: {keystone_id}")
