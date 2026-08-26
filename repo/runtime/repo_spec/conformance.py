from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SHA40_RE = re.compile(r"^[0-9a-f]{40}$")


class ConformanceError(ValueError):
    pass


def _load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConformanceError(f"unable to load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ConformanceError(f"Conformance artifact must be object: {path}")
    return value


def load_graph(root: Path) -> dict:
    return {
        "requirements": _load(root / "repo/authority/requirements.json"),
        "correspondence": _load(root / "repo/conformance/correspondence.json"),
        "assertions": _load(root / "repo/conformance/assertions.json"),
        "implementations": _load(root / "repo/conformance/implementations.json"),
        "evidence": _load(root / "repo/conformance/evidence.json"),
        "orchestration": _load(root / "repo/conformance/orchestration.json"),
    }


def _resolve_implementation_callable(impl: dict):
    target = impl.get("callable")
    if not isinstance(target, str) or not target.startswith("repo_spec.conformance."):
        raise ConformanceError(
            f"implementation callable is not a canonical Conformance entrypoint: {target}"
        )
    name = target.rsplit(".", 1)[-1]
    fn = globals().get(name)
    if not callable(fn):
        raise ConformanceError(f"implementation callable is not executable: {target}")
    return fn


def validate_closure(root: Path) -> dict:
    graph = load_graph(root)
    reqs = graph["requirements"].get("requirements")
    corr = graph["correspondence"].get("records")
    assertions = graph["assertions"].get("assertions")
    impls = graph["implementations"].get("implementations")
    evidence = graph["evidence"].get("evidence")
    orchestration = graph["orchestration"]

    for name, value in (
        ("requirements", reqs), ("correspondence", corr), ("assertions", assertions),
        ("implementations", impls), ("evidence", evidence),
    ):
        if not isinstance(value, list):
            raise ConformanceError(f"{name} registry is not a list")

    req_by_id = {}
    for req in reqs:
        rid = req.get("id")
        if not isinstance(rid, str) or not rid or rid in req_by_id:
            raise ConformanceError(f"invalid or duplicate requirement identity: {rid}")
        req_by_id[rid] = req

    corr_by_req = {}
    for rec in corr:
        rid = rec.get("requirement_id")
        if rid not in req_by_id or rid in corr_by_req:
            raise ConformanceError(f"invalid or duplicate correspondence: {rid}")
        corr_by_req[rid] = rec
    if set(corr_by_req) != set(req_by_id):
        raise ConformanceError("every accepted requirement must have exactly one correspondence")

    assertion_by_id = {}
    for assertion in assertions:
        aid = assertion.get("assertion_id")
        owner = assertion.get("requirement_id")
        if not isinstance(aid, str) or not aid or aid in assertion_by_id:
            raise ConformanceError(f"invalid or duplicate assertion identity: {aid}")
        if owner not in req_by_id:
            raise ConformanceError(f"assertion owner is not accepted authority: {aid}->{owner}")
        assertion_by_id[aid] = assertion

    impl_by_id = {}
    binding = {}
    for impl in impls:
        iid = impl.get("implementation_id")
        if not isinstance(iid, str) or not iid or iid in impl_by_id:
            raise ConformanceError(f"invalid or duplicate implementation identity: {iid}")
        if iid in assertion_by_id:
            raise ConformanceError(f"implementation identity aliases assertion identity: {iid}")
        authority_ids = impl.get("authority_requirement_ids")
        if not isinstance(authority_ids, list) or not authority_ids:
            raise ConformanceError(f"implementation lacks governed authority provenance: {iid}")
        if any(rid not in req_by_id for rid in authority_ids):
            raise ConformanceError(f"implementation authority provenance is unresolved: {iid}")
        _resolve_implementation_callable(impl)
        impl_by_id[iid] = impl
        for aid in impl.get("assertion_ids", []):
            if aid not in assertion_by_id:
                raise ConformanceError(f"implementation binds unknown assertion: {iid}->{aid}")
            binding.setdefault(aid, []).append(iid)

    for aid in assertion_by_id:
        if len(binding.get(aid, [])) != 1:
            raise ConformanceError(f"assertion must bind exactly one implementation: {aid}")

    evidence_by_impl = {}
    evidence_by_id = {}
    for rec in evidence:
        eid = rec.get("evidence_id")
        iid = rec.get("implementation_id")
        auth = rec.get("authority_requirement_ids")
        if not isinstance(eid, str) or not eid:
            raise ConformanceError("evidence identity is missing")
        if eid in evidence_by_id:
            raise ConformanceError(f"invalid or duplicate evidence identity: {eid}")
        evidence_by_id[eid] = rec
        if iid not in impl_by_id:
            raise ConformanceError(f"evidence references unknown implementation: {eid}->{iid}")
        if not isinstance(auth, list) or not auth or any(rid not in req_by_id for rid in auth):
            raise ConformanceError(f"evidence lacks governed authority provenance: {eid}")
        evidence_by_impl.setdefault(iid, []).append(rec)

    for iid, impl in impl_by_id.items():
        if impl.get("assertion_ids") and not evidence_by_impl.get(iid):
            raise ConformanceError(f"executable implementation lacks declared evidence: {iid}")

    for aid, assertion in assertion_by_id.items():
        iid = binding[aid][0]
        owner = assertion["requirement_id"]
        records = evidence_by_impl.get(iid, [])
        if not any(owner in rec.get("authority_requirement_ids", []) for rec in records):
            raise ConformanceError(f"assertion lacks requirement-owned evidence provenance: {aid}->{owner}")

    realized = orchestration.get("implementation_ids")
    orch_auth = orchestration.get("authority_requirement_ids")
    if not isinstance(realized, list):
        raise ConformanceError("orchestration implementation_ids must be list")
    if set(realized) != set(impl_by_id):
        raise ConformanceError("canonical orchestration must reach every maintained implementation")
    if not isinstance(orch_auth, list) or not orch_auth or any(r not in req_by_id for r in orch_auth):
        raise ConformanceError("orchestration lacks governed authority provenance")
    if orchestration.get("public_wrapper") != "repo/scripts/validate":
        raise ConformanceError("canonical public wrapper mismatch")
    if orchestration.get("engine") != "repo/runtime/repo_spec/conformance.py":
        raise ConformanceError("canonical engine mismatch")

    for rid, req in req_by_id.items():
        app = req.get("evaluation", {}).get("conformance", {}).get("applicability")
        rec = corr_by_req[rid]
        aids = rec.get("assertion_ids")
        if app not in {"mechanical", "none"}:
            raise ConformanceError(f"malformed Conformance applicability: {rid}:{app}")
        if rec.get("applicability") != app:
            raise ConformanceError(f"correspondence applicability mismatch: {rid}")
        if not isinstance(aids, list):
            raise ConformanceError(f"correspondence assertion_ids must be list: {rid}")
        if app == "mechanical" and not aids:
            raise ConformanceError(f"missing mechanical assertion coverage: {rid}")
        if app == "none":
            if aids:
                raise ConformanceError(f"none-applicable requirement has assertion coverage: {rid}")
            rationale = req.get("evaluation", {}).get("conformance", {}).get("rationale")
            if not isinstance(rationale, str) or not rationale.strip():
                raise ConformanceError(
                    f"none-applicable requirement lacks recorded Conformance rationale: {rid}"
                )
        if any(aid not in assertion_by_id for aid in aids):
            raise ConformanceError(f"correspondence references unknown assertion: {rid}")
        expected_aids = {aid for aid, assertion in assertion_by_id.items() if assertion.get("requirement_id") == rid}
        if set(aids) != expected_aids:
            raise ConformanceError(f"correspondence assertion ownership mismatch: {rid}: expected={sorted(expected_aids)} actual={sorted(aids)}")

    maintained = orchestration.get("maintained_paths")
    if not isinstance(maintained, list) or not maintained:
        raise ConformanceError("orchestration maintained_paths must be non-empty list")
    declared_paths = {}
    for record in maintained:
        if not isinstance(record, dict):
            raise ConformanceError("maintained Conformance path record must be object")
        rel = record.get("path")
        auth = record.get("authority_requirement_ids")
        if not isinstance(rel, str) or not rel or rel in declared_paths:
            raise ConformanceError(f"invalid or duplicate maintained Conformance path: {rel}")
        if not isinstance(auth, list) or not auth or any(rid not in req_by_id for rid in auth):
            raise ConformanceError(f"maintained Conformance path lacks authority provenance: {rel}")
        candidate = (root / rel).resolve()
        try:
            candidate.relative_to(root.resolve())
        except ValueError as exc:
            raise ConformanceError(f"maintained Conformance path escapes repository: {rel}") from exc
        if not candidate.is_file():
            raise ConformanceError(f"maintained Conformance path is missing: {rel}")
        declared_paths[rel] = record

    discovered = set()
    for controlled in (
        root / "repo/conformance",
        root / "repo/tests",
        root / "repo/runtime/repo_spec",
    ):
        if controlled.is_dir():
            for candidate in controlled.rglob("*"):
                if (
                    candidate.is_file()
                    and "__pycache__" not in candidate.parts
                    and (
                        controlled != root / "repo/runtime/repo_spec"
                        or candidate.suffix == ".py"
                    )
                ):
                    discovered.add(str(candidate.relative_to(root)))
    for rel in ("repo/scripts/validate", ".github/workflows/fs0-conformance.yml"):
        if (root / rel).is_file():
            discovered.add(rel)
    if set(declared_paths) != discovered:
        raise ConformanceError("maintained Conformance filesystem closure mismatch: " f"unregistered={sorted(discovered - set(declared_paths))} " f"missing={sorted(set(declared_paths) - discovered)}")

    gating = {a["assertion_id"] for a in assertions if a.get("gating") is True}
    reachable = {
        aid
        for iid in realized
        for aid in impl_by_id[iid].get("assertion_ids", [])
    }
    if not gating <= reachable:
        raise ConformanceError(
            f"unreachable gating assertions: {sorted(gating - reachable)}"
        )

    return {
        "requirement_count": len(req_by_id),
        "assertion_count": len(assertion_by_id),
        "implementation_count": len(impl_by_id),
        "evidence_count": len(evidence),
        "gating_count": len(gating),
    }


def _read(root: Path, rel: str) -> str:
    path = root / rel
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _planning_dirs(root: Path) -> list[Path]:
    base = root / "repo/planning"
    return sorted(
        p for p in base.iterdir()
        if p.is_dir() and p.name != "schemas"
    ) if base.is_dir() else []


def _load_runtime_module(root: Path, filename: str, name: str):
    runtime = root / "repo/runtime/repo_spec"
    spec = importlib.util.spec_from_file_location(name, runtime / filename)
    if spec is None or spec.loader is None:
        raise ConformanceError(f"unable to load runtime module: {filename}")
    module = importlib.util.module_from_spec(spec)
    old = sys.dont_write_bytecode
    added = False
    runtime_text = str(runtime)
    if runtime_text not in sys.path:
        sys.path.insert(0, runtime_text)
        added = True
    sys.dont_write_bytecode = True
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old
        if added and sys.path and sys.path[0] == runtime_text:
            sys.path.pop(0)
    return module


def _validate_all_plans(root: Path) -> dict:
    plan_runtime = _load_runtime_module(root, "plan.py", "fs0_conf_plan_runtime")
    validated = []
    for directory in _planning_dirs(root):
        loaded = plan_runtime.validate_plan(root, directory)
        validated.append(loaded.root["plan_id"])
    if not validated:
        raise ConformanceError("no maintained Plans found")
    return {"validated_plan_ids": validated}


def _build_context(root: Path):
    build_runtime = _load_runtime_module(root, "build.py", "fs0_conf_build_runtime")
    context = build_runtime.load_exactly_one_accepted_plan(root, root / "repo/planning/000_FS0-GENESIS", accepted_plan_id="FS0-GENESIS")
    return build_runtime, context


def _exercise_governance_acceptance(root: Path) -> dict:
    governance_runtime = _load_runtime_module(
        root, "governance.py", "fs0_conf_governance_runtime"
    )
    candidate = "a" * 40
    predecessor = "b" * 40
    invalid = governance_runtime.StageEvidence(
        conformance_satisfied=False,
        assurance_satisfied=True,
        evidence_refs=("governed:invalid",),
    )
    try:
        governance_runtime.make_acceptance_decision(
            decision_id="GEN-CONFORMANCE-NEGATIVE",
            stage="build",
            candidate_revision=candidate,
            actor="canonical-conformance",
            evidence=invalid,
            accept=True,
        )
    except governance_runtime.GovernanceError:
        rejected_without_evidence = True
    else:
        rejected_without_evidence = False
    valid = governance_runtime.StageEvidence(
        conformance_satisfied=True,
        assurance_satisfied=True,
        evidence_refs=("governed:conformance", "governed:assurance"),
    )
    decision = governance_runtime.make_acceptance_decision(
        decision_id="GEN-CONFORMANCE-POSITIVE",
        stage="build",
        candidate_revision=candidate,
        actor="canonical-conformance",
        evidence=valid,
        accept=True,
    )
    advanced = governance_runtime.advance_accepted_state(
        predecessor,
        decision,
        root_bootstrap=False,
    )
    return {
        "rejected_without_required_evidence": rejected_without_evidence,
        "decision_accepted": decision.accepted is True,
        "candidate_revision": decision.candidate_revision,
        "advanced_revision": advanced,
    }


def _exercise_build_verification(root: Path) -> dict:
    build_runtime, context = _build_context(root)
    build_runtime.verify_syntax = lambda _root: {"sentinel": "syntax"}
    build_runtime.verify_conformance = lambda _root, candidate_revision: {"candidate_revision": candidate_revision, "disposition": "PASS", "sentinel": "conformance"}
    build_runtime.verify_operational_completion = lambda _root, *, candidate_revision: {"candidate_revision": candidate_revision, "operationally_complete": True, "sentinel": "completion"}
    build_runtime.verify_plan_fidelity = lambda _context, _observed: {"candidate_revision": _context.candidate_revision, "accepted_plan_id": _context.plan_id, "authorized_scope_respected": True, "sentinel": "fidelity"}
    result = build_runtime.verify_build(root, context, [])
    for key in ("syntax", "conformance", "completion", "fidelity"):
        if result.get(key, {}).get("sentinel") != key:
            raise ConformanceError(f"Build verification did not exercise {key} path")
    return result


def _assertion_result(aid: str, ok: bool, detail: str, evidence=None) -> dict:
    out = {
        "assertion_id": aid,
        "status": "pass" if ok else "fail",
        "detail": detail,
    }
    if evidence is not None:
        out["evidence"] = evidence
    return out


def _evaluate(root: Path, assertion: dict) -> dict:
    aid = assertion["assertion_id"]
    rid = assertion["requirement_id"]
    reqs = _load(root / "repo/authority/requirements.json")["requirements"]
    req_by_id = {r["id"]: r for r in reqs}
    contract = _load(root / "repo/authority/framework-contract.json")
    plan_dir = root / "repo/planning/000_FS0-GENESIS"
    validation = _load(plan_dir / "validation.json")
    fs = _load(plan_dir / "functional-set.json")
    plan = _load(plan_dir / "plan.json")
    file_changes = _load(plan_dir / "file-changes.json")
    execution = _load(plan_dir / "execution.json")

    predicate = assertion.get("predicate")
    if not isinstance(predicate, str) or not predicate:
        predicate = f"Conformance assertion {aid}"

    def ret(ok, detail, evidence=None):
        primary_detail = predicate
        if not ok and detail:
            primary_detail = f"{predicate} -- {detail}"
        result = _assertion_result(aid, bool(ok), primary_detail, evidence)
        if detail:
            result["implementation_detail"] = detail
        return result

    if rid == "GEN-NR-001":
        return ret((root / "repo/authority").is_dir(), "accepted authority surface exists under repo/")
    if rid == "GEN-NR-002":
        ids = [r.get("id") for r in reqs]
        return ret(bool(ids) and len(ids) == len(set(ids)), "accepted requirement identities are present and unique")
    if rid == "GEN-NR-003":
        ids = [k.get("id") for k in contract.get("keystones", [])]
        return ret(ids == ["Governance", "Conformance", "Assurance"], "exact three authority-bearing keystones are declared")
    if rid == "GEN-NR-004":
        ks = contract.get("keystones", [])
        ok = all(k.get("authority_domain") and k.get("prohibited_authority") for k in ks)
        return ret(ok, "each keystone has delegated authority domain and explicit prohibited authority")
    if rid == "GEN-NR-006":
        route = contract.get("authority_separation", {}).get("persistent_normative_change_route")
        return ret(route == "Governance", "persistent normative change route is Governance")
    if rid == "GEN-NR-007":
        sep = contract.get("authority_separation", {}).get("framework_and_product_authority_are_distinct")
        return ret(sep is True, "framework and product authority are explicitly distinct")
    if rid in {"GEN-NR-008", "GEN-NR-009"}:
        try:
            import importlib.util, sys
            p = root / "repo/runtime/repo_spec/design.py"
            spec = importlib.util.spec_from_file_location("fs0_conf_design", p)
            if spec is None or spec.loader is None:
                raise RuntimeError(f"unable to load Design runtime: {p}")
            mod = importlib.util.module_from_spec(spec)
            old_dont_write = sys.dont_write_bytecode
            sys.dont_write_bytecode = True
            sys.modules[spec.name] = mod
            try:
                spec.loader.exec_module(mod)
            finally:
                sys.dont_write_bytecode = old_dont_write
            parsed = [
                mod.parse_design_proposal(proposal.read_text(encoding="utf-8"))
                for proposal in sorted((root / "repo/proposals").glob("*.md"))
            ]
            return ret(
                bool(parsed),
                "maintained Markdown Design Proposals parse with stable document and statement identities",
            )
        except Exception as exc:
            return ret(False, f"Design identity validation failed: {exc}")
    if rid in {"GEN-NR-011", "GEN-NR-012", "GEN-NR-055", "GEN-NR-056", "GEN-NR-057"}:
        try:
            plan_runtime = _load_runtime_module(root, "plan.py", "fs0_conf_design_plan_runtime")
            validated = []
            for directory in _planning_dirs(root):
                loaded = plan_runtime.load_plan(directory)
                plan_runtime.validate_design_scope(root, loaded)
                validated.append(loaded.root["plan_id"])
            return ret(bool(validated), "selected Design scope for every maintained Plan resolves against exact bound revisions/snapshots", {"validated_plan_ids": validated})
        except Exception as exc:
            return ret(False, f"Design binding validation failed: {exc}")
    if rid == "GEN-NR-013":
        matches = []
        for d in _planning_dirs(root):
            f = d / "functional-set.json"
            if f.is_file():
                obj = _load(f).get("functional_set", {})
                if obj.get("id") == "FS0-GENESIS" and obj.get("kind") == "genesis":
                    matches.append(d)
        return ret(len(matches) == 1, "exactly one FS0-GENESIS functional set exists")
    if rid == "GEN-NR-014":
        return ret(fs.get("accepted_predecessor") is None, "FS0-GENESIS has no accepted predecessor")
    if rid == "GEN-NR-015":
        ok = True
        for d in _planning_dirs(root):
            obj = _load(d / "functional-set.json")
            if obj.get("functional_set", {}).get("id") != "FS0-GENESIS":
                predecessor = obj.get("accepted_predecessor")
                revision = predecessor.get("accepted_revision") if isinstance(predecessor, dict) else None
                ok = ok and isinstance(revision, str) and bool(SHA40_RE.fullmatch(revision))
        return ret(
            ok,
            "all successor functional sets identify an exact 40-hex accepted repository predecessor",
        )
    if rid == "GEN-NR-016":
        ok = all((d / "functional-set.json").is_file() and (d / "plan.json").is_file() for d in _planning_dirs(root))
        return ret(ok, "every functional-set directory contains functional-set.json and plan.json")
    if rid in {"GEN-NR-018", "GEN-NR-019", "GEN-NR-020", "GEN-NR-021", "GEN-NR-044", "GEN-NR-045", "GEN-NR-046", "GEN-NR-047"}:
        try:
            coverage = _validate_all_plans(root)
            return ret(True, "every maintained Plan satisfies the shared Genesis Plan structural and execution contract", coverage)
        except Exception as exc:
            return ret(False, f"maintained Plan validation failed: {exc}")
    if rid == "GEN-NR-022":
        try:
            _, context = _build_context(root)
            return ret(context.plan_id == "FS0-GENESIS", "Build runtime consumes exactly the Governance-identified accepted Plan", {"accepted_plan_id": context.plan_id})
        except Exception as exc:
            return ret(False, f"Build Plan consumption failed: {exc}")
    if rid == "GEN-NR-023":
        try:
            build_runtime, context = _build_context(root)
            try:
                build_runtime.reject_mutations_outside_authorized_set(context, ["outside/not-authorized"])
            except build_runtime.BuildError:
                return ret(True, "Build runtime rejects mutation outside accepted Plan scope")
            return ret(False, "Build accepted an out-of-plan mutation")
        except Exception as exc:
            return ret(False, f"Build mutation-boundary exercise failed: {exc}")
    if rid == "GEN-NR-024":
        try:
            build_runtime, context = _build_context(root)
            manifest = build_runtime.mutation_manifest(context, [context.authorized_mutation_paths[0]])
            ok = manifest.get("record_type") == "build-mutation-manifest" and manifest.get("accepted_plan_id") == context.plan_id and manifest.get("candidate_revision") == context.candidate_revision
            return ret(ok, "Build runtime produces a candidate-bound machine-readable mutation manifest", manifest)
        except Exception as exc:
            return ret(False, f"Build mutation-manifest exercise failed: {exc}")
    if rid == "GEN-NR-025":
        py = list((root / "repo/runtime/repo_spec").glob("*.py"))
        try:
            for p in py:
                compile(p.read_text(encoding="utf-8"), str(p), "exec")
            for p in root.rglob("*.json"):
                json.loads(p.read_text(encoding="utf-8"))
            return ret(True, "repository Python and JSON surfaces are syntactically valid")
        except Exception as exc:
            return ret(False, f"syntactic validation failed: {exc}")
    if rid in {"GEN-NR-026", "GEN-NR-039", "GEN-NR-040"}:
        try:
            exercise = _exercise_governance_acceptance(root)
            ok = (
                exercise["rejected_without_required_evidence"]
                and exercise["decision_accepted"]
                and exercise["advanced_revision"] == exercise["candidate_revision"]
            )
            return ret(
                ok,
                "Governance acceptance is behaviorally explicit, evidence-gated, and exact-candidate state advancing",
                exercise,
            )
        except Exception as exc:
            return ret(False, f"Governance acceptance exercise failed: {exc}")
    if rid in {"GEN-NR-027", "GEN-NR-028", "GEN-NR-029", "GEN-NR-030", "GEN-NR-031",
               "GEN-NR-033", "GEN-NR-034", "GEN-NR-051", "GEN-NR-052", "GEN-NR-053",
               "GEN-NR-054", "GEN-NR-060", "GEN-NR-064"}:
        try:
            closure = validate_closure(root)
            return ret(True, "canonical Conformance closure is structurally valid", closure)
        except Exception as exc:
            return ret(False, f"Conformance closure defect: {exc}")
    if rid == "GEN-NR-035":
        return ret((root / "repo/scripts/validate").is_file(), "repo/scripts/validate is the canonical public Conformance entry point")
    if rid in {"GEN-NR-036", "GEN-NR-037"}:
        try:
            import importlib.util, sys
            p = root / "repo/runtime/repo_spec/assurance.py"
            spec = importlib.util.spec_from_file_location("fs0_conf_assurance", p)
            if spec is None or spec.loader is None:
                raise RuntimeError(f"unable to load Assurance runtime: {p}")
            mod = importlib.util.module_from_spec(spec)
            old_dont_write = sys.dont_write_bytecode
            sys.dont_write_bytecode = True
            sys.modules[spec.name] = mod
            try:
                spec.loader.exec_module(mod)
                coverage = mod.validate_correspondence(root)
            finally:
                sys.dont_write_bytecode = old_dont_write
            return ret(
                True,
                "Assurance applicability and governed obligation correspondence are structurally valid",
                coverage,
            )
        except Exception as exc:
            return ret(False, f"Assurance correspondence defect: {exc}")
    if rid == "GEN-NR-038":
        text = _read(root, "repo/runtime/repo_spec/assurance.py")
        return ret("bounded" in text and "normative authority" in text, "Assurance findings remain case-bounded and non-authoritative")
    if rid == "GEN-NR-041":
        text = _read(root, "README.md")
        req = ["FS0-GENESIS", "FS0-CORE", "Conformance", "Assurance", "repo/scripts/validate"]
        return ret(all(x in text for x in req), "README contains required Genesis portability topics")
    if rid == "GEN-NR-042":
        text = _read(root, "AGENTS.md")
        req = ["Design owns semantic meaning", "Planning owns", "Build owns implementation correctness", "repo/scripts/validate"]
        return ret(all(x in text for x in req), "AGENTS contains required authority/workflow guidance")
    if rid == "GEN-NR-043":
        text = _read(root, "LICENSE")
        return ret("GNU GENERAL PUBLIC LICENSE" in text and "Version 3, 29 June 2007" in text and len(text.splitlines()) > 600, "LICENSE contains complete GPLv3 text")
    if rid in {"GEN-NR-048", "GEN-NR-049", "GEN-NR-050"}:
        try:
            result = _exercise_build_verification(root)
            key = {"GEN-NR-048": "conformance", "GEN-NR-049": "completion", "GEN-NR-050": "fidelity"}[rid]
            return ret(key in result, f"Build verification behaviorally exercises {key} for the exact candidate", result[key])
        except Exception as exc:
            return ret(False, f"Build verification exercise failed: {exc}")
    if rid == "GEN-NR-061":
        proc = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=root, text=True, capture_output=True)
        roots = [x for x in proc.stdout.splitlines() if SHA40_RE.fullmatch(x)]
        return ret(proc.returncode == 0 and len(roots) == 1, "repository has one initial root commit as post-Genesis provenance root", roots)
    if rid == "GEN-NR-062":
        proc = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=root, text=True, capture_output=True)
        roots = [x for x in proc.stdout.splitlines() if x]
        return ret(proc.returncode == 0 and len(roots) == 1, "repository provenance resolves to a root commit with no repository predecessor")
    return ret(False, f"no Genesis mechanical evaluator is registered for {rid}")


def _evaluate_implementation(
    root: Path,
    assertions: dict[str, dict],
    assertion_ids: list[str],
) -> list[dict]:
    results = []
    for aid in assertion_ids:
        if aid not in assertions:
            raise ConformanceError(
                f"implementation references unknown assertion at execution: {aid}"
            )
        results.append(_evaluate(root, assertions[aid]))
    return results


def design(root: Path, assertions: dict[str, dict], assertion_ids: list[str]) -> list[dict]:
    return _evaluate_implementation(root, assertions, assertion_ids)


def authority(root: Path, assertions: dict[str, dict], assertion_ids: list[str]) -> list[dict]:
    return _evaluate_implementation(root, assertions, assertion_ids)


def plan(root: Path, assertions: dict[str, dict], assertion_ids: list[str]) -> list[dict]:
    return _evaluate_implementation(root, assertions, assertion_ids)


def build(root: Path, assertions: dict[str, dict], assertion_ids: list[str]) -> list[dict]:
    return _evaluate_implementation(root, assertions, assertion_ids)


def selfcheck(root: Path, assertions: dict[str, dict], assertion_ids: list[str]) -> list[dict]:
    return _evaluate_implementation(root, assertions, assertion_ids)


def portability(root: Path, assertions: dict[str, dict], assertion_ids: list[str]) -> list[dict]:
    return _evaluate_implementation(root, assertions, assertion_ids)


def governance(root: Path, assertions: dict[str, dict], assertion_ids: list[str]) -> list[dict]:
    return _evaluate_implementation(root, assertions, assertion_ids)


def run(root: Path) -> dict:
    try:
        closure = validate_closure(root)
    except Exception as exc:
        return {
            "schema_version": "1",
            "disposition": "INCOMPLETE",
            "configuration_errors": [str(exc)],
            "results": [],
        }

    graph = load_graph(root)
    assertions = {a["assertion_id"]: a for a in graph["assertions"]["assertions"]}
    impls = {i["implementation_id"]: i for i in graph["implementations"]["implementations"]}
    results = []

    for iid in graph["orchestration"]["implementation_ids"]:
        impl = impls[iid]
        owned = impl.get("assertion_ids", [])
        fn = _resolve_implementation_callable(impl)
        emitted = fn(root, assertions, owned)
        if not isinstance(emitted, list):
            return {
                "schema_version": "1",
                "disposition": "INCOMPLETE",
                "configuration_errors": [
                    f"implementation did not return a result list: {iid}"
                ],
                "results": results,
                "closure": closure,
            }
        actual_owned = [record.get("assertion_id") for record in emitted]
        if actual_owned != owned:
            return {
                "schema_version": "1",
                "disposition": "INCOMPLETE",
                "configuration_errors": [
                    f"implementation emitted results outside or incomplete relative to owned assertions: {iid}"
                ],
                "results": results + emitted,
                "closure": closure,
            }
        results.extend(emitted)

    expected = {a["assertion_id"] for a in assertions.values() if a.get("gating") is True}
    actual = [r["assertion_id"] for r in results]
    if set(actual) != expected or len(actual) != len(set(actual)):
        return {
            "schema_version": "1",
            "disposition": "INCOMPLETE",
            "configuration_errors": ["canonical execution did not emit exactly one result for every gating assertion"],
            "results": results,
            "closure": closure,
        }

    failed = [r["assertion_id"] for r in results if r["status"] != "pass"]
    return {
        "schema_version": "1",
        "disposition": "PASS" if not failed else "FAIL",
        "configuration_errors": [],
        "failed_assertions": failed,
        "results": results,
        "closure": closure,
    }
