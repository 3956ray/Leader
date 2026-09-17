import copy
import tempfile
import unittest
import json
import subprocess
import sys
from pathlib import Path

from scripts.leader_loop import transition, reference


class LoopTest(unittest.TestCase):
    def setUp(self):
        self.p = {"threads": {"developer": "01dev", "product_manager": "01pm"}}
        self.b = {"revision": 0, "task": {"task_id": "old", "phase": "suspended"},
                  "state": {"current_checkpoint": "CP2", "dispatch_hold": True},
                  "task_ids": ["old"], "archived_tasks": [], "events": []}
        self.n = {"task_id": "probe", "kind": "coordination_probe", "owner": "developer",
                  "assigned_thread_id": "01dev", "checkpoint": "CP2",
                  "goal": "Verify receipt without touching the product"}
        for key in ("scope", "out_of_scope", "acceptance", "evidence_required", "stop_conditions"):
            self.n[key] = ["test"]

    def step(self, action, data=None):
        self.b = transition(self.b, self.p, action, data or {}, "2026-09-06T00:00:00Z")

    def stage(self):
        self.step("stage", {"contract": self.n, "executor_idle": True})

    def sent(self):
        self.stage()
        self.step("send-intent")
        self.step("sent", {"delivery_success": True})

    def receipt(self):
        t = self.b["task"]
        return {**{k: t[k] for k in ("task_id", "assigned_thread_id", "attempt_id", "contract_sha256")},
                "acknowledged": True, "turn_id": "turn", "result": "COMPLETE"}

    def test_full_loop(self):
        self.sent()
        r = self.receipt()
        self.step("ack", r)
        self.step("result", r)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "evidence"
            p.write_text("verified")
            self.step("review", {"verdict": "accepted", "checks": {"identity": True},
                                 "evidence": [reference(p)]})
        self.assertEqual(self.b["state"]["state"], "ACCEPTED")
        self.assertEqual(self.b["state"]["last_developer_result"]["task_id"], "probe")
        self.assertEqual(len(self.b["events"]), 6)
        self.n["task_id"] = "next"
        self.stage()
        self.assertEqual(self.b["task"]["task_id"], "next")

    def test_no_duplicate_send(self):
        self.stage()
        self.step("send-intent")
        with self.assertRaises(ValueError):
            self.step("send-intent")

    def test_resume_requires_failed_turn_and_keeps_contract_identity(self):
        self.sent()
        receipt = self.receipt()
        self.step("ack", receipt)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observation"
            path.write_text("Prior turn failed; user authorized continuation; delivered")
            data = {**receipt, "previous_turn_id": "turn", "observed_previous_failed": True,
                    "user_requested": True, "delivery_success": True, "evidence": [reference(path)]}
            for change in ({"previous_turn_id": "other"}, {"observed_previous_failed": False},
                           {"user_requested": False}, {"delivery_success": False}, {"attempt_id": "other"}):
                with self.assertRaises(ValueError): self.step("resume", {**data, **change})
            self.step("resume", data)
            self.assertEqual(self.b["task"]["previous_execution_turns"], ["turn"])
            self.step("ack", {**receipt, "turn_id": "continued"})
            self.step("result", {**receipt, "turn_id": "continued"})
            self.assertEqual(self.b["task"]["contract_sha256"], receipt["contract_sha256"])

    def test_approved_sequence_requires_exact_pair_canonical_hash_and_accepted_predecessor(self):
        self.p["checkpoints"] = ["CP2", "CP3"]
        self.n["checkpoint"] = "CP3"
        self.b["task"].update(owner="developer")
        with tempfile.TemporaryDirectory() as directory:
            decision = Path(directory) / "approved-plan.md"
            decision.write_text("APPROVED: old CP2 then probe CP3")
            ref = reference(decision)
            self.p["approved_sequence"] = [{"previous_task_id": "old", "task_id": "probe",
                "from": "CP2", "to": "CP3", "evidence": [ref]}]
            self.p["canonical_sources"] = [ref["path"]]
            with self.assertRaises(ValueError): self.stage()
            self.b["task"]["phase"] = "accepted"
            self.p["canonical_sources"] = []
            with self.assertRaises(ValueError): self.stage()
            self.p["canonical_sources"] = [ref["path"]]
            decision.write_text("changed")
            with self.assertRaises(ValueError): self.stage()
            decision.write_text("APPROVED: old CP2 then probe CP3")
            self.n["task_id"] = "unapproved"
            with self.assertRaises(ValueError): self.stage()
            self.n["task_id"] = "probe"
            self.stage()
            self.assertEqual(self.b["state"]["current_checkpoint"], "CP3")

    def test_acknowledged_artifact_recovery_preserves_turn_binding(self):
        self.sent()
        receipt = self.receipt()
        self.step("ack", receipt)
        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory) / "result.json"
            result.write_text("COMPLETE")
            data = {**receipt, "observed_completed": True, "recovery_reason": "Final display empty",
                    "evidence": [reference(result)]}
            with self.assertRaises(ValueError):
                self.step("reconcile-result", {**data, "turn_id": "other"})
            self.step("reconcile-result", data)
            self.assertEqual(self.b["task"]["phase"], "review")
            self.assertFalse(self.b["task"]["acknowledgement_observed"])

    def test_checkpoint_change_requires_accepted_pm_evidence(self):
        self.n["checkpoint"] = "CP3"
        with self.assertRaises(ValueError):
            self.stage()
        self.p["checkpoints"] = ["CP2", "CP3"]
        self.b["task"].update(phase="accepted", owner="product_manager")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "decision"
            p.write_text("Limited text-first approval; CP2 not passed")
            ref = reference(p)
            data = {"executor_idle": True, "contract": self.n,
                    "checkpoint_reconciliation": {"decision_task_id": "old", "from": "CP2",
                        "to": "CP3", "scope_note": "Text only; no checkpoint passed", "evidence": [ref]}}
            with self.assertRaises(ValueError):
                self.step("stage", data)
            self.b["events"].append({"action": "review", "task_id": "old",
                                     "data": {"evidence": [ref], "verdict": "accepted"}})
            original = copy.deepcopy(self.b)
            p.write_text("Changed decision")
            with self.assertRaises(ValueError):
                self.step("stage", data)
            self.assertEqual(self.b, original)
            p.write_text("Limited text-first approval; CP2 not passed")
            self.step("stage", data)
            self.assertEqual(self.b["state"]["current_checkpoint"], "CP3")
            self.assertNotIn("CP2", self.b["state"].get("checkpoint_evidence", {}))

    def test_uncertain_send_can_block_not_resend(self):
        self.stage()
        self.step("send-intent")
        self.step("block", {"reason": "Delivery outcome unknown"})
        with self.assertRaises(ValueError):
            self.step("send-intent")
        self.assertEqual(self.b["state"]["state"], "PAUSED")

    def test_string_ack_is_not_boolean(self):
        self.sent()
        r = self.receipt()
        r["acknowledged"] = "true"
        with self.assertRaises(ValueError):
            self.step("ack", r)

    def test_late_receipt_resolves_block_without_resend(self):
        self.sent()
        r = self.receipt()
        self.step("block", {"reason": "Empty read"})
        with self.assertRaises(ValueError):
            self.step("ack", r)
        r["receipt_recovered"] = True
        self.step("ack", r)
        self.step("result", r)
        self.assertEqual(self.b["task"]["phase"], "review")
        self.assertEqual(self.b["task"]["resolved_blocker"], "Empty read")
        self.assertEqual(len(self.b["state"]["dispatch_history"]), 1)

    def test_hold_cannot_be_released_early(self):
        with self.assertRaises(ValueError):
            self.step("release-hold", {"evidence": []})

    def test_interactive_retires_timer_without_changing_task(self):
        self.b["state"]["scheduler_heartbeat"] = {"status": "ACTIVE", "automation_id": "old"}
        original = copy.deepcopy(self.b["task"])
        self.step("interactive", {"user_requested": True})
        self.assertNotIn("scheduler_heartbeat", self.b["state"])
        self.assertFalse(self.b["state"]["automatic_scheduling_allowed"])
        self.assertEqual(self.b["task"], original)
        with self.assertRaises(ValueError):
            self.step("scheduler", {"status": "ACTIVE", "tool_confirmed": True})

    def test_blocked_result_cannot_be_accepted(self):
        self.sent()
        r = self.receipt()
        self.step("ack", r)
        r["result"] = "BLOCKED"
        self.step("result", r)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "evidence"
            p.write_text("blocked")
            with self.assertRaises(ValueError):
                self.step("review", {"verdict": "accepted", "checks": {"identity": True},
                                     "evidence": [reference(p)]})

    def test_no_task_overwrite(self):
        self.stage()
        self.n["task_id"] = "other"
        with self.assertRaises(ValueError):
            self.stage()

    def test_no_cross_checkpoint(self):
        self.n["checkpoint"] = "CP3"
        with self.assertRaises(ValueError):
            self.stage()

    def test_no_stale_route(self):
        self.n["assigned_thread_id"] = "olddev"
        with self.assertRaises(ValueError):
            self.stage()

    def test_product_hold(self):
        self.n["kind"] = "product"
        with self.assertRaises(ValueError):
            self.stage()

    def test_no_result_before_ack(self):
        self.sent()
        with self.assertRaises(ValueError):
            self.step("result", self.receipt())

    def test_wrong_receipt(self):
        self.sent()
        r = self.receipt()
        for key in ("task_id", "assigned_thread_id", "attempt_id", "contract_sha256"):
            bad = copy.deepcopy(r)
            bad[key] = "wrong"
            with self.assertRaises(ValueError):
                self.step("ack", bad)

    def test_no_unverified_acceptance(self):
        self.sent()
        r = self.receipt()
        self.step("ack", r)
        self.step("result", r)
        with self.assertRaises(ValueError):
            self.step("review", {"verdict": "accepted"})

    def test_failed_check_rejects_acceptance(self):
        self.sent()
        r = self.receipt()
        self.step("ack", r)
        self.step("result", r)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "evidence"
            p.write_text("verified")
            with self.assertRaises(ValueError):
                self.step("review", {"verdict": "accepted", "checks": {"identity": False},
                                     "evidence": [reference(p)]})

    def test_evidence_tampering(self):
        self.sent()
        r = self.receipt()
        self.step("ack", r)
        self.step("result", r)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "evidence"
            p.write_text("verified")
            ref = reference(p)
            p.write_text("changed")
            with self.assertRaises(ValueError):
                self.step("review", {"verdict": "accepted", "checks": {"identity": True},
                                     "evidence": [ref]})

    def test_rejection_allows_scoped_next_task(self):
        self.sent()
        r = self.receipt()
        self.step("ack", r)
        self.step("result", r)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "evidence"
            p.write_text("failed")
            self.step("review", {"verdict": "rejected", "checks": {"identity": False},
                                 "evidence": [reference(p)]})
        self.n["task_id"] = "retry"
        self.stage()
        self.assertEqual(self.b["task"]["phase"], "ready")

    def test_cli_mirror_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "current-task.json").write_text(json.dumps({"task_id": "legacy"}))
            (root / "state.json").write_text(json.dumps({"current_checkpoint": "CP2"}))
            (root / "project.json").write_text(json.dumps(self.p))
            script = Path(__file__).resolve().parents[1] / "scripts/leader_loop.py"
            def run(action):
                return subprocess.run([sys.executable, str(script), action, "--root", str(root)],
                                      capture_output=True, text=True)
            self.assertEqual(run("init").returncode, 0)
            self.assertNotEqual(run("init").returncode, 0)
            (root / "state.json").write_text("{}")
            self.assertNotEqual(run("send-intent").returncode, 0)
            self.assertEqual(run("recover").returncode, 0)
            self.assertEqual(json.loads((root / "state.json").read_text()), {"current_checkpoint": "CP2"})

    def test_file_receipt_recovery_does_not_invent_ack(self):
        self.sent()
        r = self.receipt()
        r.pop("acknowledged")
        with self.assertRaises(ValueError):
            self.step("reconcile-result", r)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "report"
            p.write_text("COMPLETE: verified artifact evidence")
            r.update(observed_completed=True, recovery_reason="Original turn empty twice",
                     evidence=[reference(p)])
            self.step("reconcile-result", r)
        self.assertEqual(self.b["task"]["phase"], "review")
        self.assertFalse(self.b["task"]["acknowledgement_observed"])
        self.assertNotIn("acknowledged_at", self.b["task"])
