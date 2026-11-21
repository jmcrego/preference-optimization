"""CPU-only checks for the repository scaffold."""

import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts.scratch_paths import DEFAULT_SCRATCH_DIR, scratch_dir

ROOT = Path(__file__).resolve().parents[1]


class ScratchTests(unittest.TestCase):
    def test_default(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(scratch_dir(), DEFAULT_SCRATCH_DIR)

    def test_absolute_override(self):
        with patch.dict(os.environ, {"SCRATCH_DIR": "/example/test-scratch"}):
            self.assertEqual(scratch_dir(), Path("/example/test-scratch"))

    def test_relative_override_is_rejected(self):
        with patch.dict(os.environ, {"SCRATCH_DIR": "relative/path"}):
            with self.assertRaisesRegex(ValueError, "absolute path"):
                scratch_dir()

    def test_shell_setup_creates_scratch_directories(self):
        config = (ROOT / "configs/base.yaml").read_text()
        self.assertIn(f"  scratch_default: {DEFAULT_SCRATCH_DIR}\n", config)
        with TemporaryDirectory() as directory:
            scratch = Path(directory) / "project scratch"
            result = subprocess.run(
                ["bash", "-c", "source scripts/setup_environment.sh"],
                cwd=ROOT,
                env=dict(os.environ, SCRATCH_DIR=str(scratch), PROJECT_VENV=""),
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn(str(scratch), result.stdout)
            self.assertTrue((scratch / "datasets/prepared").is_dir())
            self.assertFalse((scratch / "logs").exists())
            self.assertTrue((scratch / "caches/huggingface/hub").is_dir())


class StageTests(unittest.TestCase):
    def test_stage_entry_points_exit_as_stubs(self):
        stages = [
            ROOT / "04_preference_dataset/run.py",
            ROOT / "05_fine_tuning/train_dpo.py",
            ROOT / "06_evaluation/evaluate.py",
            ROOT / "07_analysis/analyze.py",
        ]
        self.assertEqual([stage.parent.name[:2] for stage in stages],
                         [f"{index:02}" for index in range(4, 8)])
        for stage in stages:
            with self.subTest(stage=stage.parent.name):
                self.assertTrue(stage.with_name("README.md").is_file())
                result = subprocess.run(
                    [sys.executable, stage], cwd=ROOT, capture_output=True, text=True
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn("Phase 1 stub", result.stderr)
