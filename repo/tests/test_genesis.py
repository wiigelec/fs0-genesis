from __future__ import annotations

import copy
import importlib.util
import json
import os
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
        fs = json.loads((fixture / "functional-set.json").read_text(encoding="utf-8"))
        plan = json.loads((fixture / "plan.json").read_text(encoding="utf-8"))
        pred = fs["accepted_predecessor"]["accepted_revision"]
        self.assertRegex(pred, r"^[0-9a-f]{40}$")
        self.assertNotEqual(fs["functional_set"]["id"], "FS0-GENESIS")
        bindings = plan["design_bindings"]
        self.assertTrue(bindings)
        self.assertTrue(all(b["binding_kind"] == "repository-native" for b in bindings))
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

if __name__ == "__main__":
    unittest.main()
