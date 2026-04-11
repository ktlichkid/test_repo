import tempfile
import shutil
from pathlib import Path
import unittest

from task_tracker.repo import TaskRepository
from task_tracker.service import TaskService


class TaskTrackerFlowsTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.store = self.tmpdir / ".tasks.json"
        self.svc = TaskService(TaskRepository(self.store))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_add_and_list_persistence(self):
        t1 = self.svc.add("alpha")
        t2 = self.svc.add("beta")
        t3 = self.svc.add("gamma")
        self.assertEqual([t.id for t in [t1, t2, t3]], [1, 2, 3])
        # reload and ensure tasks persist in order
        svc2 = TaskService(TaskRepository(self.store))
        tasks = svc2.list()
        self.assertEqual(len(tasks), 3)
        self.assertFalse(tasks[0].completed)
        self.assertEqual(tasks[1].description, "beta")

    def test_complete_and_validation(self):
        self.svc.add("alpha")
        self.svc.add("beta")
        done = self.svc.complete(2)
        self.assertTrue(done.completed)
        self.assertIsNotNone(done.completed_at)
        # completing again should error
        with self.assertRaises(ValueError):
            self.svc.complete(2)
        # invalid id should error
        with self.assertRaises(ValueError):
            self.svc.complete(42)

    def test_delete_and_validation(self):
        self.svc.add("alpha")
        self.svc.add("beta")
        removed = self.svc.delete(1)
        self.assertEqual(removed.id, 1)
        # now list should only have id 2
        ids = [t.id for t in self.svc.list()]
        self.assertEqual(ids, [2])
        # invalid id should error
        with self.assertRaises(ValueError):
            self.svc.delete(99)


if __name__ == "__main__":
    unittest.main()
