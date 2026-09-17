"""Local coordination ledger. Tools deliver messages; this module records evidence."""
from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import uuid


def read(path):
    return json.loads(Path(path).read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def atomic(path, value):
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def reference(path):
    p = Path(path).resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def verify_reference(ref):
    if reference(ref["path"]) != ref:
        raise ValueError("Evidence changed: " + ref["path"])


def transition(book, project, action, data, now):
    b = copy.deepcopy(book)
    t, s = b["task"], b["state"]
    if action == "park":
        if not data.get("pm_idle") or not data.get("dev_idle"):
            raise ValueError("Both executor idle observations required")
        if t.get("phase") == "suspended":
            raise ValueError("Already parked")
        t.update(status="draft", phase="suspended")
        s.update(state="PAUSED", parked_task_id=t["task_id"])
    elif action == "stage":
        if t.get("phase") not in ("accepted", "rejected", "suspended"):
            raise ValueError("Previous task is not terminal or explicitly parked")
        if not data.get("executor_idle"):
            raise ValueError("Fresh idle observation required")
        n = copy.deepcopy(data["contract"])
        if n["task_id"] in b["task_ids"]:
            raise ValueError("Duplicate task ID")
        for key in ("goal", "scope", "out_of_scope", "acceptance", "evidence_required", "stop_conditions"):
            if not n.get(key):
                raise ValueError("Missing contract field: " + key)
        approved_step = next((step for step in project.get("approved_sequence", [])
                              if step.get("previous_task_id") == t["task_id"]
                              and step.get("task_id") == n["task_id"]
                              and step.get("from") == s["current_checkpoint"]
                              and step.get("to") == n["checkpoint"]), None)
        if n["checkpoint"] != s["current_checkpoint"] and approved_step:
            if t.get("phase") != "accepted" or not approved_step.get("evidence"):
                raise ValueError("Approved sequence requires accepted predecessor and evidence")
            if n["checkpoint"] not in project.get("checkpoints", []):
                raise ValueError("Unknown approved checkpoint")
            for ref in approved_step["evidence"]:
                if ref["path"] not in project.get("canonical_sources", []):
                    raise ValueError("Sequence evidence must be a canonical product decision")
                verify_reference(ref)
            s["current_checkpoint"] = n["checkpoint"]
            s["checkpoint_reconciliation"] = copy.deepcopy(approved_step)
        elif n["checkpoint"] != s["current_checkpoint"]:
            reconciliation = data.get("checkpoint_reconciliation", {})
            if (t.get("phase") != "accepted" or t.get("owner") != "product_manager"
                    or reconciliation.get("decision_task_id") != t["task_id"]
                    or reconciliation.get("from") != s["current_checkpoint"]
                    or reconciliation.get("to") != n["checkpoint"]
                    or n["checkpoint"] not in project.get("checkpoints", [])
                    or not reconciliation.get("scope_note")
                    or not reconciliation.get("evidence")):
                raise ValueError("Checkpoint change requires accepted PM reconciliation")
            review = next((e for e in reversed(b["events"])
                           if e["action"] == "review" and e["task_id"] == t["task_id"]), None)
            for ref in reconciliation["evidence"]:
                verify_reference(ref)
                if not review or ref not in review["data"].get("evidence", []):
                    raise ValueError("Checkpoint evidence was not accepted in PM review")
            s["current_checkpoint"] = n["checkpoint"]
            s["checkpoint_reconciliation"] = copy.deepcopy(reconciliation)
        if n["owner"] not in ("product_manager", "developer"):
            raise ValueError("Invalid executor role")
        if n["assigned_thread_id"] != project["threads"][n["owner"]]:
            raise ValueError("Stale executor route")
        if s.get("dispatch_hold") and n.get("kind") != "coordination_probe":
            raise ValueError("Product dispatch is held")
        b["archived_tasks"].append(t)
        n.update(contract_body=copy.deepcopy(n), contract_sha256=digest(n), attempt_id=str(uuid.uuid4()),
                 phase="ready", status="ready")
        b["task_ids"].append(n["task_id"])
        b["task"] = t = n
        s.update(active_task_id=n["task_id"], state="READY_FOR_DISPATCH")
    elif action == "resume":
        if (t.get("phase") != "acknowledged" or data.get("previous_turn_id") != t.get("executor_turn_id")
                or data.get("observed_previous_failed") is not True or data.get("user_requested") is not True
                or data.get("delivery_success") is not True or not data.get("evidence")):
            raise ValueError("Resume requires failed prior turn, explicit user request and verified delivery")
        for key in ("task_id", "attempt_id", "contract_sha256", "assigned_thread_id"):
            if data.get(key) != t.get(key):
                raise ValueError("Resume identity mismatch: " + key)
        for ref in data["evidence"]:
            verify_reference(ref)
        t.setdefault("previous_execution_turns", []).append(t.pop("executor_turn_id"))
        t.update(phase="sent", status="dispatched", resumed_at=now)
        s["state"] = "IN_PROGRESS"
    elif action == "send-intent":
        if t.get("phase") != "ready":
            raise ValueError("Cannot send again; reconcile existing delivery")
        if t["assigned_thread_id"] != project["threads"][t["owner"]]:
            raise ValueError("Executor route changed")
        if s.get("dispatch_hold") and t.get("kind") != "coordination_probe":
            raise ValueError("Dispatch held")
        t.update(phase="sending", status="dispatched", send_intent_at=now)
        s["state"] = "IN_PROGRESS"
    elif action == "sent":
        if t.get("phase") != "sending" or not data.get("delivery_success"):
            raise ValueError("Successful tool delivery evidence required")
        t.update(phase="sent", sent_at=now)
        s["last_dispatch"] = {"task_id": t["task_id"], "thread_id": t["assigned_thread_id"],
                              "attempt_id": t["attempt_id"], "sent_at": now}
        s.setdefault("dispatch_history", []).append(s["last_dispatch"])
    elif action in ("ack", "result"):
        expected = "sent" if action == "ack" else "acknowledged"
        late_ack = (action == "ack" and t.get("phase") == "blocked"
                    and data.get("receipt_recovered") is True and t.get("sent_at")
                    and not t.get("executor_turn_id"))
        if t.get("phase") != expected and not late_ack:
            raise ValueError("Unexpected receipt phase")
        for key in ("task_id", "attempt_id", "contract_sha256", "assigned_thread_id"):
            if data.get(key) != t.get(key):
                raise ValueError("Receipt identity mismatch: " + key)
        if not data.get("turn_id") or data.get("acknowledged") is not True:
            raise ValueError("Observed executor acknowledgment required")
        if action == "ack":
            if late_ack:
                t["resolved_blocker"] = t.pop("blocker")
            t.update(phase="acknowledged", status="dispatched", acknowledged_at=now, executor_turn_id=data["turn_id"])
            s["state"] = "IN_PROGRESS"
        else:
            if data["turn_id"] != t["executor_turn_id"]:
                raise ValueError("Different execution turn")
            if data.get("result") not in ("COMPLETE", "BLOCKED", "PRODUCT_DECISION_REQUIRED"):
                raise ValueError("Invalid result")
            t.update(phase="review", status="completed", result=data["result"], result_at=now)
            s["state"] = "AWAITING_REVIEW"
            if t["owner"] == "developer":
                s["last_developer_result"] = {"task_id": t["task_id"], "RESULT": data["result"]}
    elif action == "reconcile-result":
        if t.get("phase") not in ("sent", "blocked", "acknowledged") or data.get("observed_completed") is not True:
            raise ValueError("Completed executor observation required for file recovery")
        if t.get("executor_turn_id") and t["executor_turn_id"] != data.get("turn_id"):
            raise ValueError("Different execution turn")
        for key in ("task_id", "attempt_id", "contract_sha256", "assigned_thread_id"):
            if data.get(key) != t.get(key):
                raise ValueError("Recovered result identity mismatch: " + key)
        if not data.get("turn_id") or not data.get("evidence") or not data.get("recovery_reason"):
            raise ValueError("Turn, retained evidence and explicit recovery reason required")
        for ref in data["evidence"]:
            verify_reference(ref)
        if data.get("result") not in ("COMPLETE", "BLOCKED", "PRODUCT_DECISION_REQUIRED"):
            raise ValueError("Invalid recovered result")
        t.update(phase="review", status="completed", result=data["result"], result_at=now,
                 executor_turn_id=data["turn_id"], receipt_method="artifact_reconciliation",
                 acknowledgement_observed=False)
        s["state"] = "AWAITING_REVIEW"
        if t["owner"] == "developer":
            s["last_developer_result"] = {"task_id": t["task_id"], "RESULT": data["result"],
                                          "receipt_method": "artifact_reconciliation"}
    elif action == "upgrade-contracts":
        for item in [t, *b["archived_tasks"]]:
            if item.get("contract_sha256") and "contract_body" not in item:
                event = next(e for e in b["events"] if e["action"] == "stage" and e["task_id"] == item["task_id"])
                body = event["data"]["contract"]
                if digest(body) != item["contract_sha256"]:
                    raise ValueError("Historical contract digest mismatch")
                item["contract_body"] = copy.deepcopy(body)
    elif action == "block":
        if t.get("phase") not in ("sending", "sent", "acknowledged", "review") or not data.get("reason"):
            raise ValueError("Active phase and concrete blocking reason required")
        t.update(phase="blocked", status="draft", blocker=data["reason"])
        s["state"] = "PAUSED"
    elif action == "interactive":
        if data.get("user_requested") is not True:
            raise ValueError("Explicit user coordination preference required")
        old = s.pop("scheduler_heartbeat", None)
        if old:
            s["historical_scheduler"] = {**old, "status": "DELETED_BY_USER"}
        s["coordination_mode"] = "interactive_callback_and_wait"
        s["automatic_scheduling_allowed"] = False
    elif action == "release-hold":
        accepted = {x["task_id"] for x in [*b["archived_tasks"], t] if x.get("phase") == "accepted"}
        if not {"LOOP-V2-PM-PROBE-001", "LOOP-V2-DEV-PROBE-001"}.issubset(accepted):
            raise ValueError("Both live probes must be accepted")
        if not data.get("evidence"):
            raise ValueError("Rebuild verification evidence required")
        for ref in data["evidence"]:
            verify_reference(ref)
        s.pop("dispatch_hold", None)
        s["resume_note"] = "Coordination probes accepted; next reconcile parked product task and existing authorization before product dispatch."
    elif action == "review":
        if t.get("phase") != "review":
            raise ValueError("No result available to review")
        verdict = data.get("verdict")
        if verdict not in ("accepted", "rejected", "blocked"):
            raise ValueError("Invalid review verdict")
        if not data.get("checks") or not data.get("evidence"):
            raise ValueError("Review checks and file evidence required")
        for ref in data["evidence"]:
            verify_reference(ref)
        if verdict == "accepted" and (t.get("result") != "COMPLETE" or
                                       not all(v is True for v in data["checks"].values())):
            raise ValueError("Incomplete or failed result cannot be accepted")
        t.update(phase=verdict, status={"accepted": "accepted", "rejected": "rejected", "blocked": "draft"}[verdict])
        s["state"] = {"accepted": "ACCEPTED", "rejected": "REVISE", "blocked": "PAUSED"}[verdict]
        if verdict == "accepted":
            s["last_accepted_task_id"] = t["task_id"]
    else:
        raise ValueError("Unknown action")
    s["updated_at"] = now
    b["revision"] += 1
    b["events"].append({"revision": b["revision"], "at": now, "action": action,
                        "task_id": t["task_id"], "data": data})
    return b


def sync(root, book):
    atomic(root / "current-task.json", book["task"])
    atomic(root / "state.json", book["state"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["init", "recover", "park", "stage", "send-intent", "sent", "ack", "result", "review", "status", "block", "interactive", "release-hold", "upgrade-contracts", "reconcile-result", "resume"])
    parser.add_argument("--input", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1] / "orchestration")
    args = parser.parse_args()
    root = args.root.resolve()
    with (root / ".loop.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        path = root / "loop-ledger.json"
        if args.action == "init":
            if path.exists():
                raise ValueError("Already initialized")
            task, state = read(root / "current-task.json"), read(root / "state.json")
            book = {"revision": 0, "task": task, "state": state, "events": [],
                    "task_ids": [task["task_id"]], "archived_tasks": [],
                    "legacy_snapshot": {"task": copy.deepcopy(task), "state": copy.deepcopy(state)}}
        else:
            book = read(path)
            if args.action == "status":
                print(json.dumps({"revision": book["revision"], "task": book["task"]}, ensure_ascii=False))
                return
            if args.action != "recover":
                if read(root / "current-task.json") != book["task"] or read(root / "state.json") != book["state"]:
                    raise ValueError("Mirror drift: inspect external changes before recover")
                data = read(args.input) if args.input else {}
                if args.input:
                    data["input_evidence"] = reference(args.input)
                book = transition(book, read(root / "project.json"), args.action, data,
                                  datetime.now(timezone.utc).isoformat())
        # One atomic authoritative commit; interrupted mirror writes are detected, never silently used.
        atomic(path, book)
        sync(root, book)
        print(json.dumps({"revision": book["revision"], "action": args.action,
                          "task_id": book["task"]["task_id"], "phase": book["task"].get("phase")}))


if __name__ == "__main__":
    main()
