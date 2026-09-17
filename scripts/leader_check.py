#!/usr/bin/env python3
"""Validate Leader's local orchestration contract before dispatch."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_TASK_LISTS = (
    "scope",
    "out_of_scope",
    "acceptance",
    "evidence_required",
    "stop_conditions",
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} 顶层必须是 JSON 对象")
    return value


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    orchestration = root / "orchestration"

    try:
        project = load_json(orchestration / "project.json")
        state = load_json(orchestration / "state.json")
        task = load_json(orchestration / "current-task.json")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [str(exc)]

    checkpoints = project.get("checkpoints", [])
    states = project.get("state_values", [])
    task_statuses = project.get("task_status_values", [])
    task_owners = project.get("task_owner_values", [])

    if state.get("current_checkpoint") not in checkpoints:
        errors.append("state.current_checkpoint 不在项目 Checkpoint 列表中")
    if state.get("state") not in states:
        errors.append("state.state 不是允许的状态")
    if task.get("checkpoint") != state.get("current_checkpoint"):
        errors.append("当前任务与当前 Checkpoint 不一致")
    if task.get("task_id") != state.get("active_task_id"):
        errors.append("当前任务 ID 与状态账本不一致")
    if task.get("status") not in task_statuses:
        errors.append("current-task.status 不是允许的状态")
    if task.get("owner") not in task_owners:
        errors.append("current-task.owner 不是允许的执行者")

    goal = task.get("goal")
    if not isinstance(goal, str) or len(goal.strip()) < 20:
        errors.append("任务 goal 必须是明确、可判断且不少于 20 个字符的结果")
    elif any(term in goal for term in ("持续开发整个", "开发整个 App", "完成所有功能")):
        errors.append("任务 goal 范围过大，必须缩小到单个 Checkpoint 内的单一结果")

    for field in REQUIRED_TASK_LISTS:
        value = task.get(field)
        if not isinstance(value, list) or not value or not all(
            isinstance(item, str) and item.strip() for item in value
        ):
            errors.append(f"current-task.{field} 必须是非空字符串列表")

    expected_pairs = {
        "ready": "READY_FOR_DISPATCH",
        "dispatched": "IN_PROGRESS",
        "completed": "AWAITING_REVIEW",
        "accepted": "ACCEPTED",
        "rejected": "REVISE",
    }
    expected_state = expected_pairs.get(task.get("status"))
    if expected_state and state.get("state") != expected_state:
        errors.append(
            f"任务状态 {task.get('status')} 要求 state.state 为 {expected_state}"
        )

    for source in project.get("canonical_sources", []):
        path = Path(source)
        if not path.is_absolute():
            errors.append(f"正式来源必须使用绝对路径：{source}")
        elif not path.is_file():
            errors.append(f"正式来源不存在或不可读：{source}")

    thread_ids = project.get("threads", {})
    assigned = task.get("assigned_thread_id")
    if assigned and assigned != thread_ids.get(task.get("owner")):
        errors.append("任务执行者与当前角色路由不一致")
    ledger_path = orchestration / "loop-ledger.json"
    if ledger_path.exists():
        try:
            ledger = load_json(ledger_path)
            if ledger.get("task") != task or ledger.get("state") != state:
                errors.append("权威账本与状态视图不一致；先核对再恢复")
            phases = {"ready": "ready", "sending": "dispatched", "sent": "dispatched",
                      "acknowledged": "dispatched", "review": "completed", "accepted": "accepted",
                      "rejected": "rejected", "blocked": "draft", "suspended": "draft"}
            if task.get("phase") not in phases or phases[task["phase"]] != task["status"]:
                errors.append("调度阶段与任务状态不一致")
            if task.get("phase") != "suspended":
                body = task.get("contract_body")
                encoded = json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
                if not isinstance(body, dict) or hashlib.sha256(encoded).hexdigest() != task.get("contract_sha256"):
                    errors.append("合同摘要不匹配")
                elif any(task.get(k) != v for k, v in body.items()):
                    errors.append("冻结合同字段被修改")
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    for role in ("product_manager", "developer"):
        value = thread_ids.get(role)
        if not isinstance(value, str) or not value.startswith("01"):
            errors.append(f"缺少有效的 {role} 任务 ID")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Leader 项目根目录",
    )
    args = parser.parse_args()

    errors = validate(args.root.resolve())
    if errors:
        print("Leader 检查失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Leader 检查通过：当前任务合同、状态和正式来源一致。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
