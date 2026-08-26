from __future__ import annotations

import hashlib
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

STATEMENT_LINE_RE = re.compile(r"^\*\*((?:DP)[^*\\n]+)\*\*\s*$", re.MULTILINE)
STATEMENT_ID_RE = re.compile(r"^DP[0-9]{3}-[A-Z][A-Z0-9-]*-[0-9]{3}$")
DOC_ID_RE = re.compile(r"^DP-[0-9]{3}$")
SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class DesignError(ValueError):
    pass


@dataclass(frozen=True)
class DesignProposal:
    metadata: dict[str, object]
    statement_ids: tuple[str, ...]
    text: str


def _parse_front_matter(text: str) -> dict[str, object]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise DesignError("Design Proposal must begin with YAML-style front matter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise DesignError("Design Proposal front matter is not closed") from exc

    metadata: dict[str, object] = {}
    current_list: str | None = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current_list:
            value = raw[4:].strip()
            existing = metadata.setdefault(current_list, [])
            if not isinstance(existing, list):
                raise DesignError(f"front matter key is not a list: {current_list}")
            existing.append(value)
            continue
        if ":" not in raw:
            raise DesignError(f"unsupported front matter line: {raw}")
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise DesignError("empty front matter key")
        if value:
            metadata[key] = value.strip("\"'")
            current_list = None
        else:
            metadata[key] = []
            current_list = key
    return metadata


def parse_design_proposal(text: str) -> DesignProposal:
    metadata = _parse_front_matter(text)
    doc_id = metadata.get("doc_id")
    if not isinstance(doc_id, str) or not DOC_ID_RE.fullmatch(doc_id):
        raise DesignError("Design Proposal requires a valid doc_id")

    statement_ids = tuple(STATEMENT_LINE_RE.findall(text))
    if not statement_ids:
        raise DesignError("Design Proposal contains no explicit statement IDs")
    expected_prefix = doc_id.replace("-", "") + "-"
    for statement_id in statement_ids:
        if not STATEMENT_ID_RE.fullmatch(statement_id):
            raise DesignError(f"malformed Design statement identity: {statement_id}")
        if not statement_id.startswith(expected_prefix):
            raise DesignError(
                f"Design statement identity does not derive from proposal identity: {statement_id}"
            )
    if len(statement_ids) != len(set(statement_ids)):
        raise DesignError("Design Proposal statement IDs must be unique")

    return DesignProposal(metadata=metadata, statement_ids=statement_ids, text=text)


def _repo_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise DesignError(f"path escapes repository root: {relative}") from exc
    return candidate


def load_genesis_snapshot(root: Path, design_input: dict) -> DesignProposal:
    binding = design_input.get("binding")
    if not isinstance(binding, dict) or binding.get("kind") != "genesis-portable-snapshot":
        raise DesignError("Genesis Design input requires genesis-portable-snapshot binding")

    snapshot_path = binding.get("snapshot_path")
    digest = binding.get("content_digest")
    if not isinstance(snapshot_path, str) or not snapshot_path:
        raise DesignError("Genesis snapshot_path is required")
    if not isinstance(digest, dict):
        raise DesignError("Genesis content_digest is required")
    if digest.get("algorithm") != "sha256":
        raise DesignError("Genesis snapshot digest algorithm must be sha256")
    expected = digest.get("value")
    if not isinstance(expected, str) or not SHA256_RE.fullmatch(expected):
        raise DesignError("Genesis snapshot SHA-256 digest is malformed")

    path = _repo_path(root, snapshot_path)
    raw = path.read_bytes()
    observed = hashlib.sha256(raw).hexdigest()
    if observed != expected:
        raise DesignError(
            f"Genesis Design snapshot digest mismatch: expected {expected}, observed {observed}"
        )

    proposal = parse_design_proposal(raw.decode("utf-8"))
    if proposal.metadata.get("doc_id") != design_input.get("doc_id"):
        raise DesignError("Genesis Design snapshot doc_id mismatch")
    return proposal


def load_repository_revision(
    root: Path, design_input: dict, revision: str | None = None
) -> DesignProposal:
    binding = design_input.get("binding")
    if not isinstance(binding, dict):
        raise DesignError("Design input binding is required")
    kind = binding.get("kind")
    if kind == "genesis-portable-snapshot":
        return load_genesis_snapshot(root, design_input)
    if kind != "repository-native":
        raise DesignError(f"unsupported ordinary Design binding kind: {kind}")

    bound_revision = binding.get("revision")
    if not isinstance(bound_revision, str) or not SHA40_RE.fullmatch(bound_revision):
        raise DesignError("repository-native Design binding requires exact 40-hex repository revision")
    if revision is not None:
        if not isinstance(revision, str) or not SHA40_RE.fullmatch(revision):
            raise DesignError("requested Design revision must be exact 40-hex repository revision")
        if revision != bound_revision:
            raise DesignError("requested Design revision does not match repository-native binding")

    object_type = subprocess.run(
        ["git", "cat-file", "-t", bound_revision],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if object_type.returncode or object_type.stdout.strip() != "commit":
        raise DesignError(
            "repository-native Design revision must identify a commit object"
        )
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", bound_revision, "HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if ancestry.returncode != 0:
        raise DesignError(
            "repository-native Design revision must remain in governed repository history"
        )

    path = design_input.get("path")
    if not isinstance(path, str) or not path:
        raise DesignError("Design input path is required")

    proc = subprocess.run(
        ["git", "show", f"{bound_revision}:{path}"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if proc.returncode:
        raise DesignError(
            f"unable to retrieve Design Proposal {path} at {bound_revision}: {proc.stderr.strip()}"
        )
    proposal = parse_design_proposal(proc.stdout)
    if proposal.metadata.get("doc_id") != design_input.get("doc_id"):
        raise DesignError("repository Design revision doc_id mismatch")
    return proposal


def resolve_selected_statements(root: Path, design_input: dict) -> tuple[str, ...]:
    proposal = load_repository_revision(root, design_input)
    selected = design_input.get("statements")
    if not isinstance(selected, list) or not selected or not all(
        isinstance(item, str) and item for item in selected
    ):
        raise DesignError("Design input statements must be a non-empty string list")
    if len(selected) != len(set(selected)):
        raise DesignError("selected Design statement IDs must be unique")

    available = set(proposal.statement_ids)
    missing = [item for item in selected if item not in available]
    if missing:
        raise DesignError(f"selected Design statements are absent from bound revision: {missing}")
    return tuple(selected)
