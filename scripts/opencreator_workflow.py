#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
from typing import Any, Dict

import requests

BASE_URL = os.environ.get("OPENCREATOR_WORKFLOW_BASE", "https://dev-railway.opencreator.io")
API_KEY = os.environ.get("OPENCREATOR_API_KEY")


def die(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def headers() -> Dict[str, str]:
    if not API_KEY:
        die("OPENCREATOR_API_KEY is not set")
    return {"X-API-Key": API_KEY, "Content-Type": "application/json"}


def req(method: str, path: str, **kwargs):
    url = BASE_URL.rstrip("/") + path
    r = requests.request(method, url, headers=headers(), timeout=60, **kwargs)
    if not r.ok:
        print(r.text, file=sys.stderr)
        die(f"HTTP {r.status_code} for {url}")
    return r.json()


def get_parameters(flow_id: str) -> Dict[str, Any]:
    return req("GET", f"/api/developer/v1/workflows/{flow_id}/parameters")


def start_run(flow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    payload = {"inputs": inputs, "start_ids": [], "end_ids": []}
    return req("POST", f"/api/developer/v1/workflows/{flow_id}/runs", json=payload)


def get_status(task_id: str) -> Dict[str, Any]:
    return req("GET", f"/api/developer/v1/workflow-runs/{task_id}")


def get_results(task_id: str) -> Dict[str, Any]:
    return req("GET", f"/api/developer/v1/workflow-runs/{task_id}/results")


def poll_until_done(task_id: str, interval: float = 5.0, timeout: float = 900.0) -> Dict[str, Any]:
    start = time.time()
    last_status = None
    while True:
        status = get_status(task_id)
        cur = status.get("status")
        if cur != last_status:
            print(json.dumps({"task_id": task_id, "status": cur, "node_statuses": status.get("node_statuses", {})}, ensure_ascii=False))
            last_status = cur
        if cur == "success":
            return get_results(task_id)
        if cur in {"failed", "error", "cancelled"}:
            die(json.dumps(status, ensure_ascii=False, indent=2))
        if time.time() - start > timeout:
            die(f"Timed out waiting for task {task_id}")
        time.sleep(interval)


def parse_inputs(value: str) -> Dict[str, Any]:
    if os.path.exists(value):
        with open(value, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.loads(value)


def main():
    p = argparse.ArgumentParser(description="OpenCreator Workflow API helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("parameters")
    p1.add_argument("flow_id")

    p2 = sub.add_parser("run")
    p2.add_argument("flow_id")
    p2.add_argument("inputs", help="JSON string or path to JSON file")
    p2.add_argument("--wait", action="store_true")
    p2.add_argument("--interval", type=float, default=5.0)
    p2.add_argument("--timeout", type=float, default=900.0)

    p3 = sub.add_parser("status")
    p3.add_argument("task_id")

    p4 = sub.add_parser("results")
    p4.add_argument("task_id")

    args = p.parse_args()

    if args.cmd == "parameters":
        print(json.dumps(get_parameters(args.flow_id), ensure_ascii=False, indent=2))
    elif args.cmd == "run":
        started = start_run(args.flow_id, parse_inputs(args.inputs))
        if args.wait:
            task_id = started["task_id"]
            print(json.dumps(started, ensure_ascii=False, indent=2))
            print(json.dumps(poll_until_done(task_id, args.interval, args.timeout), ensure_ascii=False, indent=2))
        else:
            print(json.dumps(started, ensure_ascii=False, indent=2))
    elif args.cmd == "status":
        print(json.dumps(get_status(args.task_id), ensure_ascii=False, indent=2))
    elif args.cmd == "results":
        print(json.dumps(get_results(args.task_id), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
