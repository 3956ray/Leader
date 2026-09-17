import json
import tempfile
import unittest
from pathlib import Path

from scripts.leader_check import validate


class LeaderCheckTest(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "orchestration").mkdir()
        source = root / "source.md"
        source.write_text("source", encoding="utf-8")

        project = {
            "checkpoints": ["CP0"],
            "state_values": ["READY_FOR_DISPATCH", "IN_PROGRESS", "AWAITING_REVIEW", "ACCEPTED", "REVISE"],
            "task_owner_values": ["leader", "product_manager", "developer", "user"],
            "task_status_values": ["ready", "dispatched", "completed", "accepted", "rejected"],
            "canonical_sources": [str(source)],
            "threads": {"product_manager": "01pm", "developer": "01dev"},
        }
        state = {
            "current_checkpoint": "CP0",
            "state": "READY_FOR_DISPATCH",
            "active_task_id": "CP0-001",
        }
        task = {
            "task_id": "CP0-001",
            "owner": "developer",
            "checkpoint": "CP0",
            "status": "ready",
            "goal": "核对当前 Checkpoint 的所有门槛并提供可复查的证据。",
            "scope": ["读取证据"],
            "out_of_scope": ["不修改代码"],
            "acceptance": ["逐项报告"],
            "evidence_required": ["文件路径"],
            "stop_conditions": ["需要产品决定"],
        }
        for name, value in (
            ("project.json", project),
            ("state.json", state),
            ("current-task.json", task),
        ):
            (root / "orchestration" / name).write_text(
                json.dumps(value, ensure_ascii=False), encoding="utf-8"
            )
        return root

    def test_valid_contract(self) -> None:
        self.assertEqual(validate(self.make_root()), [])

    def test_rejects_checkpoint_mismatch(self) -> None:
        root = self.make_root()
        path = root / "orchestration" / "current-task.json"
        task = json.loads(path.read_text(encoding="utf-8"))
        task["checkpoint"] = "CP1"
        path.write_text(json.dumps(task), encoding="utf-8")

        errors = validate(root)

        self.assertIn("当前任务与当前 Checkpoint 不一致", errors)

    def test_rejects_vague_whole_app_goal(self) -> None:
        root = self.make_root()
        path = root / "orchestration" / "current-task.json"
        task = json.loads(path.read_text(encoding="utf-8"))
        task["goal"] = "持续开发整个 App 直到所有功能全部完成并可以发布。"
        path.write_text(json.dumps(task), encoding="utf-8")

        errors = validate(root)

        self.assertTrue(any("范围过大" in error for error in errors))

    def test_stale_executor(self):
        root = self.make_root()
        p = root / "orchestration/current-task.json"
        task = json.loads(p.read_text())
        task["assigned_thread_id"] = "01old"
        p.write_text(json.dumps(task))
        self.assertTrue(any("路由" in e for e in validate(root)))

    def test_mirror_drift(self):
        root = self.make_root()
        (root / "orchestration/loop-ledger.json").write_text(json.dumps({"task": {}, "state": {}}))
        self.assertTrue(any("权威账本" in e for e in validate(root)))


if __name__ == "__main__":
    unittest.main()
