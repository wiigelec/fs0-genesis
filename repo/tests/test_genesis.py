from __future__ import annotations

import copy
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "repo/runtime/repo_spec"
PLAN_DIR = ROOT / "repo/planning/000_FS0-GENESIS"

def load_module(name: str, filename: str):
    path = RUNTIME / filename
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    added = False
    runtime_dir = str(RUNTIME)
    if runtime_dir not in sys.path:
        sys.path.insert(0, runtime_dir)
        added = True
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old
        if added and sys.path and sys.path[0] == runtime_dir:
            sys.path.pop(0)
    return module

CONFORMANCE = load_module("fs0_test_conformance", "conformance.py")
GOVERNANCE = load_module("fs0_test_governance", "governance.py")
ASSURANCE = load_module("fs0_test_assurance", "assurance.py")
BUILD = load_module("fs0_test_build", "build.py")
PLAN = load_module("fs0_test_plan", "plan.py")

class GenesisEvidence(unittest.TestCase):
    def temp_repo_copy(self, *, include_git: bool = False):
        td = tempfile.TemporaryDirectory(prefix="fs0-genesis-test-")
        dst = Path(td.name) / "repo-copy"
        ignore = None if include_git else shutil.ignore_patterns(".git")
        shutil.copytree(ROOT, dst, ignore=ignore)
        return td, dst

    def mutate_json(self, root: Path, relpath: str, mutator):
        path = root / relpath
        data = json.loads(path.read_text(encoding="utf-8"))
        mutator(data)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def test_canonical_validation_passes_locally_without_github_api(self):
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        for key in list(env):
            if key.startswith("GITHUB_"):
                env.pop(key, None)
        cp = subprocess.run([str(ROOT / "repo/scripts/validate")], cwd=ROOT, text=True, capture_output=True, env=env)
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertEqual(cp.stdout.strip(), "FS0 Conformance: PASS")

    def test_genesis_design_snapshots_verify_without_prototype_git_history(self):
        td, copied = self.temp_repo_copy(include_git=False)
        self.addCleanup(td.cleanup)
        self.assertFalse((copied / ".git").exists())
        loaded = PLAN.load_plan(copied / "repo/planning/000_FS0-GENESIS")
        PLAN.validate_design_scope(copied, loaded)

    def test_preserved_snapshot_does_not_replace_maintained_design_source(self):
        fsdoc = json.loads((PLAN_DIR / "functional-set.json").read_text(encoding="utf-8"))
        design_inputs = fsdoc.get("design_inputs", [])
        self.assertTrue(design_inputs)
        for design_input in design_inputs:
            binding = design_input["binding"]
            snapshot = ROOT / binding["snapshot_path"]
            maintained = ROOT / design_input["path"]
            self.assertTrue(snapshot.is_file())
            self.assertTrue(maintained.is_file())
            self.assertNotEqual(snapshot.resolve(), maintained.resolve())
        design = load_module("fs0_test_design", "design.py")
        parsed = [design.parse_design_proposal(path.read_text(encoding="utf-8")) for path in sorted((ROOT / "repo/proposals").glob("*.md"))]
        self.assertTrue(parsed)

    def test_successor_fixture_uses_exact_predecessor_and_repository_native_binding(self):
        fixture = ROOT / "repo/tests/fixtures/successor"
        loaded = PLAN.validate_plan(ROOT, fixture)
        fs = loaded.functional_set
        pred = fs["accepted_predecessor"]["accepted_revision"]
        self.assertRegex(pred, r"^[0-9a-f]{40}$")
        self.assertNotEqual(fs["functional_set"]["id"], "FS0-GENESIS")
        bindings = [item["binding"] for item in fs["design_inputs"]]
        self.assertTrue(bindings)
        self.assertTrue(all(b["kind"] == "repository-native" for b in bindings))
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{40}", b["revision"]) for b in bindings))
        self.assertTrue(all("snapshot_path" not in b for b in bindings))

    def test_successor_predecessor_requires_exact_revision_object(self):
        loaded = PLAN.load_plan(PLAN_DIR)
        documents = dict(loaded.documents)
        successor = copy.deepcopy(loaded.functional_set)
        successor["functional_set"]["id"] = "FS1-PREDECESSOR-TEST"
        successor["functional_set"]["kind"] = "successor"
        successor["accepted_predecessor"] = {"accepted_revision": "a" * 40}
        documents["functional_set"] = successor
        candidate = PLAN.LoadedPlan(loaded.directory, loaded.root, documents)
        PLAN.validate_predecessor_rules(candidate)

        for bad in (
            None,
            "a" * 40,
            {},
            {"accepted_revision": "not-a-sha"},
            {"accepted_revision": "a" * 39},
        ):
            successor_bad = copy.deepcopy(successor)
            successor_bad["accepted_predecessor"] = bad
            bad_docs = dict(documents)
            bad_docs["functional_set"] = successor_bad
            bad_candidate = PLAN.LoadedPlan(loaded.directory, loaded.root, bad_docs)
            with self.assertRaises(PLAN.PlanError):
                PLAN.validate_predecessor_rules(bad_candidate)

    def test_conformance_rejects_missing_none_applicability_rationale(self):
        td, copied = self.temp_repo_copy()
        self.addCleanup(td.cleanup)

        def mutate(data):
            for requirement in data["requirements"]:
                conformance = requirement.get("evaluation", {}).get("conformance", {})
                if conformance.get("applicability") == "none":
                    conformance.pop("rationale", None)
                    return
            self.fail("no Conformance-none requirement found")

        self.mutate_json(copied, "repo/authority/requirements.json", mutate)
        with self.assertRaises(CONFORMANCE.ConformanceError):
            CONFORMANCE.validate_closure(copied)

    def test_canonical_conformance_detects_broken_assurance_correspondence(self):
        td, copied = self.temp_repo_copy()
        self.addCleanup(td.cleanup)

        def mutate(data):
            for record in data["records"]:
                if record.get("applicability") == "required":
                    record["obligation_ids"] = ["GEN-OBL-DOES-NOT-EXIST"]
                    return
            self.fail("no required Assurance correspondence found")

        self.mutate_json(copied, "repo/assurance/correspondence.json", mutate)
        report = CONFORMANCE.run(copied)
        self.assertEqual(report["disposition"], "FAIL")
        failed = set(report.get("failed_assertions", []))
        self.assertIn("GEN-ASSERT-036", failed)
        self.assertIn("GEN-ASSERT-037", failed)

    def test_build_rejects_out_of_plan_mutation_and_emits_manifest(self):
        context = BUILD.load_exactly_one_accepted_plan(ROOT, PLAN_DIR, accepted_plan_id="FS0-GENESIS")
        with self.assertRaises(BUILD.BuildError):
            BUILD.reject_mutations_outside_authorized_set(context, ["outside/not-authorized"])
        manifest = BUILD.mutation_manifest(context, ["repo/tests/"])
        self.assertEqual(manifest["record_type"], "build-mutation-manifest")
        self.assertEqual(manifest["accepted_plan_id"], "FS0-GENESIS")

    def test_build_verification_rejects_nonpassing_conformance(self):
        for disposition in ("FAIL", "INCOMPLETE"):
            build = load_module(
                f"fs0_test_build_nonpassing_{disposition.lower()}",
                "build.py",
            )
            context = build.load_exactly_one_accepted_plan(
                ROOT,
                PLAN_DIR,
                accepted_plan_id="FS0-GENESIS",
            )
            build.verify_syntax = lambda _root: {"sentinel": "syntax"}
            build.verify_conformance = (
                lambda _root, candidate_revision, disposition=disposition: {
                    "candidate_revision": candidate_revision,
                    "disposition": disposition,
                }
            )
            with self.assertRaises(build.BuildError):
                build.verify_build(ROOT, context, [])

    def test_canonical_conformance_behaviorally_enforces_assurance_boundary(self):
        report = CONFORMANCE.run(ROOT)
        result = next(
            item
            for item in report["results"]
            if item["assertion_id"] == "GEN-ASSERT-038"
        )
        self.assertEqual(result["status"], "pass")
        evidence = result["evidence"]
        self.assertTrue(evidence["valid_case_accepted"])
        self.assertTrue(evidence["normative_change_rejected"])

    def test_governance_candidate_binding_and_platform_non_authority(self):
        revision = "a" * 40
        surface = GOVERNANCE.ReviewSurface(issue_id="42", candidate_revision=revision, candidate_branch="candidate/test", pull_request_id="43", pull_request_branch="candidate/test", pull_request_revision=revision)
        GOVERNANCE.validate_review_surface(surface, root_bootstrap=False)
        bad = GOVERNANCE.ReviewSurface(issue_id="42", candidate_revision=revision, candidate_branch="candidate/test", pull_request_id="43", pull_request_branch="candidate/test", pull_request_revision="b" * 40)
        with self.assertRaises(GOVERNANCE.GovernanceError):
            GOVERNANCE.validate_review_surface(bad, root_bootstrap=False)
        events = [
            "issue-open",
            "issue-close",
            "pull-request-open",
            "pull-request-review",
            "pull-request-merge",
            "workflow-pass",
            "workflow-fail",
            "comment",
        ]
        self.assertFalse(GOVERNANCE.platform_activity_creates_acceptance(events))

    def test_assurance_receipt_is_exact_candidate_case_bounded_and_non_authoritative(self):
        revision = "a" * 40
        receipt = {
            "case_id": "GEN-CASE-TEST",
            "stage": "build",
            "authorizing_authority": "Governance",
            "review_subject": {"work_id": "GEN-WORK-TEST", "candidate_revision": revision},
            "obligation_ids": ["GEN-OBL-AUTHORITY-BOUNDARY", "GEN-OBL-BUILD-FIDELITY", "GEN-OBL-ASSURANCE-BOUNDARY", "GEN-OBL-PORTABILITY-ROOT"],
            "evidence": ["conformance:test"],
            "findings": [{"finding_id": "GEN-FINDING-1", "disposition": "PASS", "statement": "bounded finding"}],
            "disposition": "PASS",
            "reviewer": "reviewer",
        }
        case = ASSURANCE.validate_receipt(ROOT, receipt, candidate_revision=revision, work_id="GEN-WORK-TEST")
        self.assertEqual(case["candidate_revision"], revision)
        bad = copy.deepcopy(receipt)
        bad["findings"][0]["normative_change"] = {"id": "BAD"}
        with self.assertRaises(ASSURANCE.AssuranceError):
            ASSURANCE.validate_review_case(ROOT, bad)

    def test_repository_has_one_post_genesis_provenance_root(self):
        cp = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(cp.returncode, 0, cp.stderr)
        roots = [line for line in cp.stdout.splitlines() if line]
        self.assertEqual(len(roots), 1)
        self.assertRegex(roots[0], r"^[0-9a-f]{40}$")

    def test_conformance_rejects_orphan_assertion(self):
        td, copied = self.temp_repo_copy()
        self.addCleanup(td.cleanup)
        def mutate(data):
            data["assertions"].append({"assertion_id":"GEN-ASSERT-ORPHAN","requirement_id":"GEN-NR-001","predicate":"orphan assertion","gating":True,"role":"assertion"})
        self.mutate_json(copied, "repo/conformance/assertions.json", mutate)
        with self.assertRaises(CONFORMANCE.ConformanceError):
            CONFORMANCE.validate_closure(copied)

    def test_conformance_rejects_orphan_implementation(self):
        td, copied = self.temp_repo_copy()
        self.addCleanup(td.cleanup)
        def mutate(data):
            data["implementations"].append({"implementation_id":"GEN-IMPL-ORPHAN","kind":"python","callable":"orphan","assertion_ids":[],"role":"support","authority_requirement_ids":[]})
        self.mutate_json(copied, "repo/conformance/implementations.json", mutate)
        with self.assertRaises(CONFORMANCE.ConformanceError):
            CONFORMANCE.validate_closure(copied)

    def test_conformance_rejects_orphan_evidence(self):
        td, copied = self.temp_repo_copy()
        self.addCleanup(td.cleanup)
        def mutate(data):
            data["evidence"].append({"evidence_id":"GEN-EVIDENCE-ORPHAN","implementation_id":"GEN-IMPL-DESIGN","evidence_class":"execution-result","role":"evidence","authority_requirement_ids":[]})
        self.mutate_json(copied, "repo/conformance/evidence.json", mutate)
        with self.assertRaises(CONFORMANCE.ConformanceError):
            CONFORMANCE.validate_closure(copied)

    def test_conformance_rejects_orphan_orchestration(self):
        td, copied = self.temp_repo_copy()
        self.addCleanup(td.cleanup)
        def mutate(data):
            data["authority_requirement_ids"] = []
        self.mutate_json(copied, "repo/conformance/orchestration.json", mutate)
        with self.assertRaises(CONFORMANCE.ConformanceError):
            CONFORMANCE.validate_closure(copied)

    def test_evidence_closure_is_independent_of_assertion_success(self):
        closure = CONFORMANCE.validate_closure(ROOT)
        report = CONFORMANCE.run(ROOT)
        self.assertGreater(closure["assertion_count"], 0)
        self.assertEqual(report["disposition"], "PASS")
        self.assertEqual(closure["assertion_count"], len(report["results"]))


    def test_design_requires_dp_nnn_document_identity(self):
        design = load_module("fs0_test_design_identity", "design.py")
        source = (ROOT / "repo/proposals/design-proposal.md").read_text(encoding="utf-8")
        bad = source.replace("doc_id: DP-001", "doc_id: BANANA", 1)
        with self.assertRaises(design.DesignError):
            design.parse_design_proposal(bad)

    def test_repository_native_design_binding_requires_exact_revision(self):
        design = load_module("fs0_test_design_binding_exact", "design.py")
        valid = {"doc_id": "DP-001", "path": "repo/proposals/design-proposal.md", "statements": ["DP001-REQUIREMENTS-003"], "binding": {"kind": "repository-native", "revision": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()}}
        design.resolve_selected_statements(ROOT, valid)
        for bad_revision in ("main", "HEAD", "fs0-0.0", "a" * 39, "a" * 41):
            bad = copy.deepcopy(valid)
            bad["binding"]["revision"] = bad_revision
            with self.assertRaises(design.DesignError):
                design.resolve_selected_statements(ROOT, bad)

    def test_plan_runtime_enforces_root_and_subdocument_contract(self):
        td, copied = self.temp_repo_copy(include_git=True)
        self.addCleanup(td.cleanup)
        copied_plan = copied / "repo/planning/000_FS0-GENESIS"
        self.mutate_json(copied, "repo/planning/000_FS0-GENESIS/plan.json", lambda data: data.pop("status", None))
        with self.assertRaises(PLAN.PlanError):
            PLAN.validate_plan(copied, copied_plan)
        shutil.copy2(PLAN_DIR / "plan.json", copied_plan / "plan.json")
        def break_change(data):
            data["changes"][0].pop("purpose", None)
        self.mutate_json(copied, "repo/planning/000_FS0-GENESIS/file-changes.json", break_change)
        with self.assertRaises(PLAN.PlanError):
            PLAN.validate_plan(copied, copied_plan)

    def test_canonical_conformance_validates_every_maintained_plan(self):
        td, copied = self.temp_repo_copy(include_git=True)
        self.addCleanup(td.cleanup)
        successor = copied / "repo/planning/001_FS1-EVIDENCE-FIXTURE"
        shutil.copytree(copied / "repo/tests/fixtures/successor", successor)
        plan_path = successor / "plan.json"
        doc = json.loads(plan_path.read_text(encoding="utf-8"))
        doc.pop("status", None)
        plan_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        report = CONFORMANCE.run(copied)
        self.assertEqual(report["disposition"], "FAIL")
        self.assertIn("GEN-ASSERT-018", set(report.get("failed_assertions", [])))

    def test_conformance_rejects_crosswired_correspondence_assertion(self):
        td, copied = self.temp_repo_copy()
        self.addCleanup(td.cleanup)
        graph = CONFORMANCE.load_graph(copied)
        assertions = graph["assertions"]["assertions"]
        records = graph["correspondence"]["records"]
        by_req = {}
        for assertion in assertions:
            by_req.setdefault(assertion["requirement_id"], []).append(assertion["assertion_id"])
        mechanical = [record for record in records if record.get("assertion_ids")]
        first = mechanical[0]
        other = next(record for record in mechanical if record["requirement_id"] != first["requirement_id"])
        replacement = by_req[other["requirement_id"]][0]
        def mutate(data):
            for record in data["records"]:
                if record["requirement_id"] == first["requirement_id"]:
                    record["assertion_ids"] = [replacement]
                    return
        self.mutate_json(copied, "repo/conformance/correspondence.json", mutate)
        with self.assertRaises(CONFORMANCE.ConformanceError):
            CONFORMANCE.validate_closure(copied)

    def test_conformance_rejects_assertion_without_requirement_owned_evidence(self):
        td, copied = self.temp_repo_copy()
        self.addCleanup(td.cleanup)
        graph = CONFORMANCE.load_graph(copied)
        assertions = {a["assertion_id"]: a for a in graph["assertions"]["assertions"]}
        target = None
        for impl in graph["implementations"]["implementations"]:
            records = [e for e in graph["evidence"]["evidence"] if e["implementation_id"] == impl["implementation_id"]]
            for aid in impl.get("assertion_ids", []):
                owner = assertions[aid]["requirement_id"]
                for record in records:
                    auth = record.get("authority_requirement_ids", [])
                    if owner in auth and len(auth) > 1:
                        target = (record["evidence_id"], owner)
                        break
                if target:
                    break
            if target:
                break
        self.assertIsNotNone(target)
        evidence_id, owner = target
        def mutate(data):
            for record in data["evidence"]:
                if record["evidence_id"] == evidence_id:
                    record["authority_requirement_ids"] = [rid for rid in record["authority_requirement_ids"] if rid != owner]
                    return
        self.mutate_json(copied, "repo/conformance/evidence.json", mutate)
        with self.assertRaises(CONFORMANCE.ConformanceError):
            CONFORMANCE.validate_closure(copied)

    def test_conformance_rejects_duplicate_evidence_identity(self):
        td, copied = self.temp_repo_copy()
        self.addCleanup(td.cleanup)
        def mutate(data):
            data["evidence"].append(copy.deepcopy(data["evidence"][0]))
        self.mutate_json(copied, "repo/conformance/evidence.json", mutate)
        with self.assertRaises(CONFORMANCE.ConformanceError):
            CONFORMANCE.validate_closure(copied)

    def test_conformance_rejects_unregistered_filesystem_primitive(self):
        td, copied = self.temp_repo_copy()
        self.addCleanup(td.cleanup)
        (copied / "repo/tests/orphan_validator.py").write_text("def enforce():\n    return True\n", encoding="utf-8")
        with self.assertRaises(CONFORMANCE.ConformanceError):
            CONFORMANCE.validate_closure(copied)

    def test_accepted_state_schema_requires_explicit_predecessor(self):
        schema = json.loads((ROOT / "repo/state/accepted-state.schema.json").read_text(encoding="utf-8"))
        self.assertIn("predecessor", schema["required"])
        predecessor = schema["properties"]["predecessor"]["oneOf"]
        self.assertTrue(any(option.get("type") == "null" for option in predecessor))
        self.assertTrue(any(option.get("type") == "string" and option.get("pattern") == "^[0-9a-f]{40}$" for option in predecessor))


    def test_design_statement_identity_uses_proposal_prefix_and_shape(self):
        design = load_module("fs0_test_design_statement_identity", "design.py")
        source = (ROOT / "repo/proposals/design-proposal.md").read_text(encoding="utf-8")
        malformed = source.replace("**DP001-STATUS-001**", "**DP001-STATUS-BAD**", 1)
        with self.assertRaises(design.DesignError):
            design.parse_design_proposal(malformed)
        wrong_proposal = source.replace("**DP001-STATUS-001**", "**DP002-STATUS-001**", 1)
        with self.assertRaises(design.DesignError):
            design.parse_design_proposal(wrong_proposal)

    def test_repository_native_design_binding_rejects_tree_object(self):
        design = load_module("fs0_test_design_commit_object", "design.py")
        tree = subprocess.run(
            ["git", "rev-parse", "HEAD^{tree}"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        design_input = {
            "doc_id": "DP-001",
            "path": "repo/proposals/design-proposal.md",
            "statements": ["DP001-REQUIREMENTS-003"],
            "binding": {"kind": "repository-native", "revision": tree},
        }
        with self.assertRaises(design.DesignError):
            design.resolve_selected_statements(ROOT, design_input)

    def test_plan_runtime_enforces_functional_set_schema_identity(self):
        td, copied = self.temp_repo_copy(include_git=True)
        self.addCleanup(td.cleanup)
        plan_dir = copied / "repo/planning/000_FS0-GENESIS"
        def mutate(data):
            data["functional_set"].pop("title", None)
        self.mutate_json(
            copied,
            "repo/planning/000_FS0-GENESIS/functional-set.json",
            mutate,
        )
        with self.assertRaises(PLAN.PlanError):
            PLAN.validate_plan(copied, plan_dir)

    def test_conformance_filesystem_closure_includes_runtime_helpers(self):
        orchestration = json.loads(
            (ROOT / "repo/conformance/orchestration.json").read_text(encoding="utf-8")
        )
        declared = {record["path"] for record in orchestration["maintained_paths"]}
        runtime_paths = {
            str(path.relative_to(ROOT))
            for path in (ROOT / "repo/runtime/repo_spec").glob("*.py")
        }
        self.assertTrue(runtime_paths <= declared)

    def test_canonical_ci_fetches_governed_history_for_successor_bindings(self):
        workflow = (ROOT / ".github/workflows/fs0-conformance.yml").read_text(encoding="utf-8")
        self.assertIn("fetch-depth: 0", workflow)

    def test_governance_canonical_behavior_rejects_missing_evidence(self):
        governance = load_module("fs0_test_governance_behavior", "governance.py")
        bad = governance.StageEvidence(
            conformance_satisfied=False,
            assurance_satisfied=True,
            evidence_refs=("test:evidence",),
        )
        with self.assertRaises(governance.GovernanceError):
            governance.make_acceptance_decision(
                decision_id="TEST-DECISION",
                stage="build",
                candidate_revision="a" * 40,
                actor="test",
                evidence=bad,
                accept=True,
            )

if __name__ == "__main__":
    unittest.main()
