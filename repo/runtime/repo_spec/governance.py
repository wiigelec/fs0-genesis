from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

SHA40_RE = re.compile(r"^[0-9a-f]{40}$")


class GovernanceError(ValueError):
    pass


@dataclass(frozen=True)
class ReviewSurface:
    issue_id: str
    candidate_revision: str
    candidate_branch: str | None = None
    pull_request_id: str | None = None
    pull_request_branch: str | None = None
    pull_request_revision: str | None = None


@dataclass(frozen=True)
class StageEvidence:
    conformance_satisfied: bool
    assurance_satisfied: bool
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class AcceptanceDecision:
    decision_id: str
    stage: str
    candidate_revision: str
    accepted: bool
    actor: str
    evidence: StageEvidence
    resulting_accepted_state: str | None


PLATFORM_EVENTS = {
    "issue-open",
    "issue-close",
    "pull-request-open",
    "pull-request-review",
    "pull-request-merge",
    "workflow-pass",
    "workflow-fail",
    "comment",
}


def _require_sha(value: str, label: str) -> None:
    if not isinstance(value, str) or not SHA40_RE.fullmatch(value):
        raise GovernanceError(f"{label} must be an exact 40-hex repository revision")


def validate_root_provenance(
    candidate_revision: str,
    predecessor_revision: str | None,
) -> None:
    _require_sha(candidate_revision, "root candidate revision")
    if predecessor_revision is not None:
        raise GovernanceError(
            "initial Genesis repository provenance revision must not require a predecessor"
        )


def validate_review_surface(surface: ReviewSurface, *, root_bootstrap: bool = False) -> None:
    if not isinstance(surface.issue_id, str) or not surface.issue_id.strip():
        raise GovernanceError("governed work requires stable issue identity")
    _require_sha(surface.candidate_revision, "candidate revision")

    if root_bootstrap:
        # G0 may be reviewed without a predecessor pull request because it is the
        # first repository-native provenance point.
        if surface.pull_request_id is None:
            return

    if surface.pull_request_id is None:
        return

    if not isinstance(surface.pull_request_id, str) or not surface.pull_request_id.strip():
        raise GovernanceError("pull-request identity must be stable when present")
    if not isinstance(surface.candidate_branch, str) or not surface.candidate_branch:
        raise GovernanceError("candidate branch is required when pull request is present")
    if surface.pull_request_branch != surface.candidate_branch:
        raise GovernanceError("pull-request branch does not match governed candidate branch")
    if surface.pull_request_revision != surface.candidate_revision:
        raise GovernanceError("pull-request revision does not match governed candidate revision")
    _require_sha(surface.pull_request_revision, "pull-request revision")


def validate_stage_evidence(evidence: StageEvidence) -> None:
    if not evidence.conformance_satisfied:
        raise GovernanceError("required Conformance evidence is not satisfied")
    if not evidence.assurance_satisfied:
        raise GovernanceError("required Assurance evidence is not satisfied")
    if not evidence.evidence_refs:
        raise GovernanceError("acceptance requires governed evidence references")
    if not all(isinstance(ref, str) and ref.strip() for ref in evidence.evidence_refs):
        raise GovernanceError("evidence references must be non-empty strings")


def make_acceptance_decision(
    *,
    decision_id: str,
    stage: str,
    candidate_revision: str,
    actor: str,
    evidence: StageEvidence,
    accept: bool,
) -> AcceptanceDecision:
    if not isinstance(decision_id, str) or not decision_id.strip():
        raise GovernanceError("acceptance decision requires stable identity")
    if stage not in {"planning", "build", "bootstrap"}:
        raise GovernanceError(f"unsupported Genesis acceptance stage: {stage}")
    _require_sha(candidate_revision, "acceptance candidate revision")
    if not isinstance(actor, str) or not actor.strip():
        raise GovernanceError("acceptance decision requires attributable actor")

    if accept:
        validate_stage_evidence(evidence)
        resulting = candidate_revision
    else:
        resulting = None

    return AcceptanceDecision(
        decision_id=decision_id,
        stage=stage,
        candidate_revision=candidate_revision,
        accepted=accept,
        actor=actor,
        evidence=evidence,
        resulting_accepted_state=resulting,
    )


def advance_accepted_state(
    current_accepted_state: str | None,
    decision: AcceptanceDecision,
    *,
    root_bootstrap: bool = False,
) -> str:
    if not decision.accepted:
        raise GovernanceError("rejected decision cannot advance accepted state")
    validate_stage_evidence(decision.evidence)
    _require_sha(decision.candidate_revision, "accepted candidate revision")

    if root_bootstrap:
        if current_accepted_state is not None:
            raise GovernanceError("bootstrap acceptance requires no prior accepted repository state")
    else:
        if current_accepted_state is None:
            raise GovernanceError("ordinary acceptance requires one accepted predecessor state")
        _require_sha(current_accepted_state, "current accepted state")

    if decision.resulting_accepted_state != decision.candidate_revision:
        raise GovernanceError("accepted decision must advance exactly to its candidate revision")
    return decision.candidate_revision


def apply_created_requirements(
    current_records: Iterable[dict],
    normative_changes: Iterable[dict],
) -> tuple[dict, ...]:
    records = [dict(record) for record in current_records]
    seen = {record.get("id") for record in records}

    for change in normative_changes:
        if change.get("operation") != "create":
            raise GovernanceError(
                "Genesis minimal Governance only applies accepted create requirement changes"
            )
        requirement = change.get("requirement")
        if not isinstance(requirement, dict):
            raise GovernanceError("normative change missing requirement")
        rid = requirement.get("id")
        if not isinstance(rid, str) or not rid:
            raise GovernanceError("accepted requirement requires stable identity")
        if rid in seen:
            raise GovernanceError(f"accepted requirement already exists: {rid}")
        seen.add(rid)
        records.append(dict(requirement))

    return tuple(records)


def platform_activity_creates_acceptance(events: Iterable[str]) -> bool:
    # Repository hosting activity is provenance/evidence only. It never creates
    # acceptance without an explicit Governance decision.
    for event in events:
        if event not in PLATFORM_EVENTS:
            raise GovernanceError(f"unknown platform activity: {event}")
    return False
