#!/usr/bin/env python3
"""DevTrack: a small JSON-backed command-line task manager."""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DATA_FILE = Path(__file__).parent / "tasks.json"


def load_tasks(data_file):
    """Load tasks, returning an empty list when the file does not exist."""
    path = Path(data_file)
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not read {path}: invalid JSON ({exc})") from exc
    if not isinstance(tasks, list):
        raise ValueError(f"{path} must contain a JSON list.")
    return tasks


def save_tasks(tasks, data_file):
    """Write tasks as readable JSON, creating parent folders if needed."""
    path = Path(data_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)
        file.write("\n")


def add_task(tasks, title, priority="medium"):
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")
    if priority not in {"low", "medium", "high"}:
        raise ValueError("Priority must be low, medium, or high.")
    task = {
        "id": uuid.uuid4().hex[:8],
        "title": title,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    tasks.append(task)
    return task


def complete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task
    raise ValueError(f"No task found with ID '{task_id}'.")


def delete_task(tasks, task_id):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            return tasks.pop(index)
    raise ValueError(f"No task found with ID '{task_id}'.")


def print_tasks(tasks):
    if not tasks:
        print("No tasks yet. Add one with: python main.py add \"Your task\"")
        return
    print(f"{'ID':<10} {'STATUS':<12} {'PRIORITY':<10} TASK")
    print("-" * 62)
    for task in tasks:
        status = "Done" if task["completed"] else "Pending"
        print(f"{task['id']:<10} {status:<12} {task['priority']:<10} {task['title']}")


def build_parser():
    parser = argparse.ArgumentParser(
        description="DevTrack - a simple command-line task manager."
    )
    parser.add_argument(
        "--file", type=Path, default=DEFAULT_DATA_FILE,
        help="Path to the JSON data file (default: tasks.json)."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add_parser = commands.add_parser("add", help="Add a task.")
    add_parser.add_argument("title", help="Task title.")
    add_parser.add_argument(
        "--priority", choices=["low", "medium", "high"], default="medium"
    )

    commands.add_parser("list", help="List all tasks.")

    done_parser = commands.add_parser("done", help="Mark a task as complete.")
    done_parser.add_argument("task_id")

    delete_parser = commands.add_parser("delete", help="Delete a task.")
    delete_parser.add_argument("task_id")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        tasks = load_tasks(args.file)

        if args.command == "add":
            task = add_task(tasks, args.title, args.priority)
            save_tasks(tasks, args.file)
            print(f"Added task {task['id']}: {task['title']}")
        elif args.command == "list":
            print_tasks(tasks)
        elif args.command == "done":
            task = complete_task(tasks, args.task_id)
            save_tasks(tasks, args.file)
            print(f"Completed: {task['title']}")
        elif args.command == "delete":
            task = delete_task(tasks, args.task_id)
            save_tasks(tasks, args.file)
            print(f"Deleted: {task['title']}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
