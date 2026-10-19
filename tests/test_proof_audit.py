"""Exercise proof-ledger failure modes; these are not mathematical proof tests."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_proof import audit


def claim(identifier="C1", status="proved", dependencies=None):
    row = {
        "id": identifier, "statement": "For every real x, x squared is nonnegative.",
        "quantifiers": "For every real x", "output_rule": "A deterministic inequality",
        "assumptions": [], "dependencies": dependencies or [], "status": status,
        "argument": "A square is a product of numbers of the same sign.",
        "gaps": [], "evidence": [{"kind": "derivation", "used_fact": "Ordered-field multiplication"}],
    }
    if status == "open":
        row["gaps"] = ["The required sign argument has not yet been supplied."]
        row["evidence"] = []
    elif status == "refuted":
        row["statement"] = "Every real square is strictly positive."
        row["counterexample"] = "At x = 0 the square is zero."
        row["evidence"] = []
    return row


def ledger(rows=None, target_id="C1"):
    rows = rows if rows is not None else [claim()]
    chosen = next(row for row in rows if row["id"] == target_id)
    return {
        "schema_version": 1,
        "target": {"requested_statement": chosen["statement"],
                   "formal_statement": chosen["statement"],
                   "quantifiers": chosen["quantifiers"],
                   "output_rule": chosen["output_rule"], "claim_id": target_id},
        "assumptions": [], "claims": rows,
    }


def source():
    return {"kind": "source", "used_fact": "The exact imported lemma",
            "reference": "https://arxiv.org/abs/2105.04026v2",
            "version": "arxiv:2105.04026v2", "locator": "A supplied lemma location",
            "checked_scope": "Only this lemma and its stated hypotheses", "checked": True}


class ProofAuditTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)

    def check_error(self, data, phrase):
        result = audit(data, self.root)
        self.assertFalse(result["ledger_consistent"])
        self.assertFalse(result["target_closed_under_given_assumptions"])
        self.assertIn(phrase, "\n".join(result["errors"]))
        self.assertEqual(result["mathematical_validity"], "not_checked")
        return result

    def artifact(self, name, content):
        path = self.root / name
        path.write_bytes(content)
        return {"path": name, "sha256": hashlib.sha256(content).hexdigest()}

    def formal(self):
        return {
            "kind": "formal", "used_fact": "The recorded declaration",
            "artifact": self.artifact("proof.lean", b"-- A recorded artifact, not executed by this test.\n"),
            "log": self.artifact("proof.log", b"Recorded prior prover output\n"),
            "toolchain": "leanprover/lean4:v4.19.0", "command": "lean proof.lean",
            "declaration": "square_nonnegative", "formal_statement": "forall x : Real, 0 <= x*x",
            "axioms": ["propext", "Classical.choice", "Quot.sound"],
            "axioms_reviewed": True, "statement_correspondence": "checked", "result": "passed",
        }

    def run_cli(self, data, *arguments):
        path = self.root / "ledger.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/audit_proof.py"),
                                 str(path), "--root", str(self.root), *arguments],
                                capture_output=True, text=True)
        self.assertNotIn("Traceback", result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_valid_self_contained_ledger_does_not_claim_mathematical_certification(self):
        result = audit(ledger(), self.root)
        self.assertTrue(result["ledger_consistent"])
        self.assertTrue(result["target_closed_under_given_assumptions"])
        self.assertEqual(result["mathematical_validity"], "not_checked")

    def test_unknown_claim_and_assumption_are_rejected(self):
        data = ledger()
        data["claims"][0]["dependencies"] = ["L404"]
        data["claims"][0]["assumptions"] = ["A404"]
        result = self.check_error(data, "unknown dependency L404")
        self.assertIn("unknown assumption A404", "\n".join(result["errors"]))

    def test_target_cannot_silently_change_claim_statement_quantifiers_or_output(self):
        for field, replacement in (("formal_statement", "Every square is strictly positive."),
                                   ("quantifiers", "With probability one, simultaneously for all times"),
                                   ("output_rule", "The last iterate rather than an average")):
            with self.subTest(field=field):
                data = ledger()
                data["target"][field] = replacement
                result = audit(data, self.root)
                self.assertFalse(result["ledger_consistent"])
                self.assertTrue(any("target" in error for error in result["errors"]))

    def test_cycle_and_long_cycle_do_not_overflow_the_call_stack(self):
        for length in (1, 3, 1200):
            with self.subTest(length=length):
                rows = [claim(f"C{i}", "open", [f"C{(i + 1) % length}"]) for i in range(length)]
                self.check_error(ledger(rows, "C0"), "cyclic claim dependency")

    def test_long_acyclic_chain_is_valid(self):
        rows = [claim("C0")]
        rows.extend(claim(f"C{i}", dependencies=[f"C{i-1}"]) for i in range(1, 1200))
        self.assertTrue(audit(ledger(rows, "C1199"), self.root)["ledger_consistent"])

    def test_closed_claim_cannot_depend_on_open_or_refuted_claim(self):
        for dependency_status in ("open", "refuted"):
            for target_status in ("proved", "conditional"):
                with self.subTest(dependency=dependency_status, target=target_status):
                    rows = [claim("L1", dependency_status), claim("C1", target_status, ["L1"])]
                    self.check_error(ledger(rows), "closed claim depends on unresolved/refuted L1")

    def test_added_assumption_cannot_be_hidden_through_dependency_chain(self):
        rows = [claim("L1", "conditional"), claim("L2", "conditional", ["L1"]),
                claim("C1", "proved", ["L2"])]
        rows[0]["assumptions"] = ["A1"]
        data = ledger(rows)
        data["assumptions"] = [{"id": "A1", "statement": "A needed regularity condition",
                                "origin": "added", "reason": "The original problem did not supply it."}]
        self.check_error(data, "silently inherits conditional dependency L2")
        rows[-1]["status"] = "conditional"
        result = audit(data, self.root)
        self.assertTrue(result["ledger_consistent"])
        self.assertFalse(result["target_closed_under_given_assumptions"])

    def test_direct_added_assumption_requires_conditional_status(self):
        data = ledger()
        data["assumptions"] = [{"id": "A1", "statement": "A new assumption", "origin": "added",
                                "reason": "Needed by the selected theorem"}]
        data["claims"][0]["assumptions"] = ["A1"]
        self.check_error(data, "requires conditional status")

    def test_closed_claim_needs_argument_and_no_open_gaps(self):
        data = ledger()
        data["claims"][0]["gaps"] = ["Interchanging a limit and expectation remains unjustified."]
        del data["claims"][0]["argument"]
        result = self.check_error(data, "closed claim still has gaps")
        self.assertIn("closed claim needs an argument", "\n".join(result["errors"]))

    def test_numerical_or_symbolic_evidence_alone_cannot_close_general_claim(self):
        for kind in ("numerical", "symbolic"):
            with self.subTest(kind=kind):
                data = ledger()
                data["claims"][0]["evidence"] = [{"kind": kind, "used_fact": "Checked a finite set of instances"}]
                self.check_error(data, "checks alone do not close")

    def test_pinned_checked_source_can_support_ledger_closure(self):
        data = ledger()
        data["claims"][0]["evidence"] = [source()]
        self.assertTrue(audit(data, self.root)["ledger_consistent"])

    def test_source_needs_version_locator_scope_and_actual_check(self):
        for field in ("version", "locator", "checked_scope", "reference", "checked"):
            with self.subTest(field=field):
                evidence = source()
                del evidence[field]
                data = ledger()
                data["claims"][0]["evidence"] = [evidence]
                self.check_error(data, "source-dependent closure" if field != "checked" else "fixed version")

    def test_unpinned_source_labels_do_not_substitute_for_fixed_identity(self):
        for version in ("latest", " latest ", "v2", "2026", "arxiv:2105.04026"):
            with self.subTest(version=version):
                evidence = source()
                evidence["version"] = version
                data = ledger()
                data["claims"][0]["evidence"] = [evidence]
                self.check_error(data, "fixed version")

    def test_modified_artifact_is_detected(self):
        evidence = source()
        evidence["artifact"] = self.artifact("source.tex", b"Original theorem")
        data = ledger()
        data["claims"][0]["evidence"] = [evidence]
        self.assertTrue(audit(data, self.root)["ledger_consistent"])
        (self.root / "source.tex").write_bytes(b"Different theorem")
        self.check_error(data, "artifact hash mismatch")

    def test_arxiv_reference_must_match_paper_and_explicit_edition(self):
        for reference, phrase in (("https://arxiv.org/abs/1705.07809v1", "different papers"),
                                  ("arxiv:2105.04026v1", "different editions"),
                                  ("https://arxiv.org/pdf/2105.04026v1.pdf", "different editions")):
            with self.subTest(reference=reference):
                evidence=source()
                evidence["reference"]=reference
                data=ledger()
                data["claims"][0]["evidence"]=[evidence]
                self.check_error(data,phrase)
        evidence=source()
        evidence["reference"]="https://arxiv.org/abs/2105.04026"
        data=ledger()
        data["claims"][0]["evidence"]=[evidence]
        self.assertTrue(audit(data,self.root)["ledger_consistent"])

    def test_doi_reference_and_pin_must_agree(self):
        evidence=source()
        evidence.update(reference="https://doi.org/10.1000/First",version="doi:10.1000/other")
        data=ledger()
        data["claims"][0]["evidence"]=[evidence]
        self.check_error(data,"DOI pin disagree")
        evidence["version"]="doi:10.1000/first"
        self.assertTrue(audit(data,self.root)["ledger_consistent"])

    def test_hash_pin_needs_a_matching_checked_artifact(self):
        evidence=source()
        evidence["version"]="sha256:"+"0"*64
        data=ledger()
        data["claims"][0]["evidence"]=[evidence]
        self.check_error(data,"requires its local artifact")
        evidence["artifact"]=self.artifact("pinned.tex",b"The exact source bytes")
        self.check_error(data,"pin and artifact digest disagree")
        evidence["version"]="sha256:"+evidence["artifact"]["sha256"]
        self.assertTrue(audit(data,self.root)["ledger_consistent"])

    def test_legacy_arxiv_category_pin_is_recognized(self):
        evidence=source()
        evidence.update(reference="https://arxiv.org/abs/math.PR/0601001v2",version="arxiv:math.PR/0601001v2")
        data=ledger()
        data["claims"][0]["evidence"]=[evidence]
        self.assertTrue(audit(data,self.root)["ledger_consistent"])

    def test_parent_absolute_and_symlink_artifact_escapes_are_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / "source.tex"
            external.write_bytes(b"External evidence")
            (self.root / "linked.tex").symlink_to(external)
            for path in ("../source.tex", str(external), "linked.tex"):
                with self.subTest(path=path):
                    evidence = source()
                    evidence["artifact"] = {"path": path, "sha256": hashlib.sha256(b"External evidence").hexdigest()}
                    data = ledger()
                    data["claims"][0]["evidence"] = [evidence]
                    self.check_error(data, "artifact escapes")

    def test_missing_artifact_is_reported(self):
        data = ledger()
        data["claims"][0]["evidence"][0]["artifact"] = {"path": "missing.tex", "sha256": "0" * 64}
        self.check_error(data, "artifact is missing or unreadable")

    def test_symlink_loop_and_nul_artifact_path_report_errors_without_crashing(self):
        (self.root / "loop.tex").symlink_to("loop.tex")
        for path in ("loop.tex", "source\x00.tex"):
            with self.subTest(path=path):
                data = ledger()
                data["claims"][0]["evidence"][0]["artifact"] = {"path": path, "sha256": "0" * 64}
                result = audit(data, self.root)
                self.assertFalse(result["ledger_consistent"])
                code, result = self.run_cli(data)
                self.assertEqual(code, 1)
                self.assertFalse(result["ledger_consistent"])

    def test_formal_placeholder_and_conclusion_as_axiom_fail(self):
        for axiom in ("sorryAx", "Namespace.sorryAx", "square_nonnegative"):
            with self.subTest(axiom=axiom):
                evidence = self.formal()
                evidence["axioms"].append(axiom)
                data = ledger()
                data["claims"][0]["evidence"] = [evidence]
                self.check_error(data, "placeholder or conclusion-as-axiom")

    def test_formal_evidence_requires_statement_alignment_and_review(self):
        for field, value in (("statement_correspondence", "unchecked"), ("axioms_reviewed", False),
                             ("result", "not_run")):
            with self.subTest(field=field):
                evidence = self.formal()
                evidence[field] = value
                data = ledger()
                data["claims"][0]["evidence"] = [evidence]
                self.check_error(data, "formal closure needs")

    def test_formal_command_is_recorded_but_never_executed(self):
        evidence = self.formal()
        marker = self.root / "evidence-command-was-executed"
        evidence["command"] = f"touch '{marker}'"
        data = ledger()
        data["claims"][0]["evidence"] = [evidence]
        code, result = self.run_cli(data, "--require-closed")
        self.assertEqual(code, 0)
        self.assertFalse(marker.exists())
        self.assertEqual(result["mathematical_validity"], "not_checked")
        self.assertTrue(any("did not run" in message for message in result["notices"]))

    def test_mixed_status_ledger_does_not_poison_unrelated_proved_target(self):
        rows = [claim(), claim("C2", "open"), claim("C3", "refuted"), claim("C4", "conditional")]
        result = audit(ledger(rows), self.root)
        self.assertTrue(result["ledger_consistent"])
        self.assertTrue(result["target_closed_under_given_assumptions"])
        self.assertEqual(result["open_claims"], ["C2"])
        self.assertEqual(result["refuted_claims"], ["C3"])
        self.assertEqual(result["conditional_claims"], ["C4"])

    def test_cli_exit_codes_distinguish_inconsistency_from_unclosed_target(self):
        for status in ("proved", "conditional", "open", "refuted"):
            with self.subTest(status=status):
                data = ledger([claim(status=status)])
                code, _ = self.run_cli(data)
                self.assertEqual(code, 0)
                code, _ = self.run_cli(data, "--require-closed")
                self.assertEqual(code, 0 if status == "proved" else 2)
        data = ledger()
        data["claims"][0]["dependencies"] = ["unknown"]
        code, result = self.run_cli(data, "--require-closed")
        self.assertEqual(code, 1)
        self.assertFalse(result["ledger_consistent"])

    def test_malformed_json_and_malformed_field_types_return_structured_cli_errors(self):
        path = self.root / "malformed.json"
        path.write_text("{not json", encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/audit_proof.py"), str(path)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)["ledger_consistent"])
        for mutation in ("origin", "kind", "status"):
            with self.subTest(field=mutation):
                data = ledger()
                if mutation == "origin":
                    data["assumptions"] = [{"id": "A1", "statement": "test", "origin": []}]
                elif mutation == "kind":
                    data["claims"][0]["evidence"][0]["kind"] = {}
                else:
                    data["claims"][0]["status"] = []
                code, result = self.run_cli(data)
                self.assertEqual(code, 1)
                self.assertFalse(result["ledger_consistent"])
                direct = audit(data, self.root)
                self.assertFalse(direct["ledger_consistent"])


if __name__ == "__main__":
    unittest.main()
