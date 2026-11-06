import json
import tempfile
import unittest
from pathlib import Path

from main import add_task, complete_task, delete_task, load_tasks, save_tasks


class DevTrackTests(unittest.TestCase):
    def test_add_task_trims_title_and_sets_defaults(self):
        tasks = []
        task = add_task(tasks, "  Write README  ")
        self.assertEqual(task["title"], "Write README")
        self.assertEqual(task["priority"], "medium")
        self.assertFalse(task["completed"])
        self.assertEqual(len(task["id"]), 8)

    def test_add_task_rejects_blank_title(self):
        with self.assertRaises(ValueError):
            add_task([], "   ")

    def test_add_task_rejects_invalid_priority(self):
        with self.assertRaises(ValueError):
            add_task([], "Fix bug", "urgent")

    def test_complete_and_delete_task(self):
        tasks = []
        task = add_task(tasks, "Run tests")
        completed = complete_task(tasks, task["id"])
        self.assertTrue(completed["completed"])
        deleted = delete_task(tasks, task["id"])
        self.assertEqual(deleted["id"], task["id"])
        self.assertEqual(tasks, [])

    def test_missing_task_raises_error(self):
        with self.assertRaises(ValueError):
            complete_task([], "missing")

    def test_json_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            tasks = [add_task([], "Ship project", "high")]
            save_tasks(tasks, path)
            self.assertEqual(load_tasks(path), tasks)

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_tasks(Path(directory) / "missing.json"), [])


if __name__ == "__main__":
    unittest.main()
