from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import json

SHA40_RE = re.compile(r"^[0-9a-f]{40}$")


class AssuranceError(ValueError):
    pass


@dataclass(frozen=True)
class Finding:
    finding_id: str
    disposition: str
    statement: str


def _load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AssuranceError(f"unable to load Assurance artifact {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AssuranceError(f"Assurance artifact must be object: {path}")
    return value


def load_obligations(root: Path) -> dict[str, dict]:
    data = _load(root / "repo/assurance/obligations.json")
    records = data.get("obligations")
    if not isinstance(records, list):
        raise AssuranceError("obligations registry requires obligations list")
    out = {}
    for record in records:
        oid = record.get("id")
        if not isinstance(oid, str) or not oid or oid in out:
            raise AssuranceError(f"invalid or duplicate obligation identity: {oid}")
        stages = record.get("stage")
        if not isinstance(stages, list) or not stages or any(s not in {"planning", "build"} for s in stages):
            raise AssuranceError(f"invalid obligation stages: {oid}")
        reqs = record.get("requirement_ids")
        if not isinstance(reqs, list) or not reqs:
            raise AssuranceError(f"obligation lacks requirement correspondence: {oid}")
        out[oid] = record
    return out


def validate_correspondence(root: Path) -> dict:
    requirements = _load(root / "repo/authority/requirements.json")["requirements"]
    correspondence = _load(root / "repo/assurance/correspondence.json")["records"]
    obligations = load_obligations(root)

    req_by_id = {r["id"]: r for r in requirements}
    corr_by_req = {}
    for rec in correspondence:
        rid = rec.get("requirement_id")
        if rid not in req_by_id or rid in corr_by_req:
            raise AssuranceError(f"invalid or duplicate Assurance correspondence: {rid}")
        corr_by_req[rid] = rec

    if set(corr_by_req) != set(req_by_id):
        raise AssuranceError("every accepted requirement must have exactly one Assurance correspondence")

    for rid, req in req_by_id.items():
        app = req.get("evaluation", {}).get("assurance", {}).get("applicability")
        rec = corr_by_req[rid]
        if rec.get("applicability") != app:
            raise AssuranceError(f"Assurance applicability mismatch: {rid}")
        oids = rec.get("obligation_ids")
        if not isinstance(oids, list):
            raise AssuranceError(f"obligation_ids must be list: {rid}")
        if app == "required" and not oids:
            raise AssuranceError(f"required Assurance coverage missing: {rid}")
        if app == "none" and oids:
            raise AssuranceError(f"none-applicable requirement has Assurance obligations: {rid}")
        for oid in oids:
            if oid not in obligations:
                raise AssuranceError(f"unknown Assurance obligation: {rid}->{oid}")
            if rid not in obligations[oid]["requirement_ids"]:
                raise AssuranceError(f"Assurance correspondence is not reciprocal: {rid}->{oid}")

    return {
        "requirement_count": len(req_by_id),
        "obligation_count": len(obligations),
        "required_count": sum(
            1
            for r in requirements
            if r.get("evaluation", {}).get("assurance", {}).get("applicability") == "required"
        ),
    }


def obligations_for_stage(root: Path, stage: str) -> tuple[dict, ...]:
    if stage not in {"planning", "build"}:
        raise AssuranceError(f"unsupported Assurance stage: {stage}")
    obligations = load_obligations(root)
    return tuple(o for o in obligations.values() if stage in o["stage"])


def validate_review_case(root: Path, case: dict) -> dict:
    contract = _load(root / "repo/assurance/review-case-contract.json")
    required = contract.get("required_fields")
    if not isinstance(required, list):
        raise AssuranceError("review-case contract missing required_fields")
    missing = [field for field in required if field not in case]
    if missing:
        raise AssuranceError(f"review case missing required fields: {missing}")

    case_id = case["case_id"]
    stage = case["stage"]
    subject = case["review_subject"]
    obligation_ids = case["obligation_ids"]
    findings = case["findings"]
    disposition = case["disposition"]
    reviewer = case["reviewer"]

    if not isinstance(case_id, str) or not case_id:
        raise AssuranceError("review case requires stable case identity")
    if stage not in {"planning", "build"}:
        raise AssuranceError("review case stage must be planning or build")
    if disposition not in contract.get("dispositions", []):
        raise AssuranceError(f"invalid Assurance disposition: {disposition}")
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise AssuranceError("review case requires attributable reviewer")
    if not isinstance(subject, dict):
        raise AssuranceError("review_subject must be object")
    candidate = subject.get("candidate_revision")
    if not isinstance(candidate, str) or not SHA40_RE.fullmatch(candidate):
        raise AssuranceError("review case must bind exact 40-hex candidate revision")
    work_id = subject.get("work_id")
    if not isinstance(work_id, str) or not work_id.strip():
        raise AssuranceError("review case must bind governed work identity")

    applicable = {o["id"] for o in obligations_for_stage(root, stage)}
    if not isinstance(obligation_ids, list) or not obligation_ids:
        raise AssuranceError("review case must identify exercised obligations")
    if any(oid not in applicable for oid in obligation_ids):
        raise AssuranceError("review case exercises obligation not applicable to stage")

    if not isinstance(case.get("evidence"), list) or not case["evidence"]:
        raise AssuranceError("review case requires evidence references")
    if not isinstance(findings, list):
        raise AssuranceError("review case findings must be list")
    for finding in findings:
        if not isinstance(finding, dict):
            raise AssuranceError("finding must be object")
        if not finding.get("finding_id") or finding.get("disposition") not in {"PASS", "FAIL", "INCOMPLETE"}:
            raise AssuranceError("finding requires stable identity and disposition")
        if "normative_change" in finding:
            raise AssuranceError(
                "Assurance findings are case-bounded and cannot directly create or amend persistent normative authority"
            )

    return {
        "case_id": case_id,
        "stage": stage,
        "candidate_revision": candidate,
        "work_id": work_id,
        "obligation_ids": tuple(obligation_ids),
        "disposition": disposition,
    }


def validate_receipt(root: Path, receipt: dict, *, candidate_revision: str, work_id: str) -> dict:
    if not isinstance(candidate_revision, str) or not SHA40_RE.fullmatch(candidate_revision):
        raise AssuranceError("expected candidate revision must be exact 40-hex SHA")
    case = validate_review_case(root, receipt)
    if case["candidate_revision"] != candidate_revision:
        raise AssuranceError("Assurance receipt candidate revision mismatch")
    if case["work_id"] != work_id:
        raise AssuranceError("Assurance receipt governed work identity mismatch")
    return case
