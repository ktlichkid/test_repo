import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout

from task_tracker.cli import main


class CLIMalformedIdTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmpdir)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def run_cli(self, argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            try:
                rc = main(argv)
            except SystemExit as e:
                rc = int(e.code)
        return rc, buf.getvalue().strip()

    def test_complete_malformed_id(self):
        rc, out = self.run_cli(["complete", "foo"])
        self.assertEqual(rc, 1)
        self.assertTrue(out.startswith("Error: Invalid id: foo"), out)

    def test_delete_non_positive_id(self):
        rc, out = self.run_cli(["delete", "0"])
        self.assertEqual(rc, 1)
        self.assertTrue(out.startswith("Error: Invalid id: 0"), out)


if __name__ == "__main__":
    unittest.main()
