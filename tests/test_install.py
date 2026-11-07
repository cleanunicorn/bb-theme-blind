import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import install


class InstallerTests(unittest.TestCase):
    def test_install_and_update_preserve_previous_versions(self):
        with tempfile.TemporaryDirectory(prefix="blind test ") as directory:
            root = Path(directory)
            source = root / "source.css"
            source.write_text("first")
            destination, backup = install.install(root / "themes", source)
            self.assertIsNone(backup)
            self.assertEqual(destination.read_text(), "first")
            source.write_text("second")
            _, backup = install.install(root / "themes", source)
            self.assertEqual(backup.read_text(), "first")
            self.assertEqual(destination.read_text(), "second")
            _, next_backup = install.install(root / "themes", source)
            self.assertNotEqual(backup, next_backup)
            self.assertEqual(backup.read_text(), "first")
            self.assertFalse(list(destination.parent.glob("*.tmp")))

    def test_failed_copy_keeps_installed_theme(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "blind" / "theme.css"
            destination.parent.mkdir()
            destination.write_text("existing")
            with self.assertRaises(FileNotFoundError):
                install.install(root, root / "missing.css")
            self.assertEqual(destination.read_text(), "existing")
            self.assertFalse(list(destination.parent.glob("*.tmp")))

    def test_cli_activation_is_optional(self):
        for flags, expected_calls in [([], 2), (["--no-activate"], 1)]:
            with self.subTest(flags=flags), tempfile.TemporaryDirectory() as directory:
                with patch("install.shutil.which", return_value="bb"), patch(
                    "install.run_bb", side_effect=[directory, "Theme set to blind"]
                ) as run, contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(install.main(flags), 0)
                self.assertEqual(run.call_count, expected_calls)
                self.assertTrue((Path(directory) / "blind" / "theme.css").is_file())
                if not flags:
                    run.assert_called_with("bb", "theme", "set", "blind")

    def test_invalid_directory_stops_before_writing(self):
        with patch("install.shutil.which", return_value="bb"), patch(
            "install.run_bb", return_value="relative/path"
        ), patch("install.install") as write, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(install.main([]), 1)
            write.assert_not_called()

    def test_missing_cli_fails_cleanly(self):
        with patch("install.shutil.which", return_value=None), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(install.main([]), 1)


if __name__ == "__main__":
    unittest.main()
