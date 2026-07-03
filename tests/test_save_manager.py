import json
import tempfile
import unittest
from pathlib import Path

from save_manager import load_best_score, update_best_score


class TestSaveManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.save_path = Path(self.temp_dir.name) / "save.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_save_file_returns_zero(self):
        self.assertEqual(load_best_score(self.save_path), 0)

    def test_update_best_score_creates_file_and_saves_score(self):
        best_score = update_best_score(self.save_path, 5)

        self.assertTrue(self.save_path.exists())
        self.assertEqual(best_score, 5)
        with self.save_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        self.assertEqual(data, {"best_score": 5})

    def test_higher_current_score_replaces_old_best_score(self):
        update_best_score(self.save_path, 3)
        best_score = update_best_score(self.save_path, 8)

        self.assertEqual(best_score, 8)
        self.assertEqual(load_best_score(self.save_path), 8)

    def test_lower_current_score_does_not_replace_old_best_score(self):
        update_best_score(self.save_path, 10)
        best_score = update_best_score(self.save_path, 4)

        self.assertEqual(best_score, 10)
        self.assertEqual(load_best_score(self.save_path), 10)

    def test_invalid_json_is_handled_safely_as_zero(self):
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        self.save_path.write_text("not valid json", encoding="utf-8")

        self.assertEqual(load_best_score(self.save_path), 0)

    def test_saved_score_can_be_loaded_correctly(self):
        update_best_score(self.save_path, 12)

        self.assertEqual(load_best_score(self.save_path), 12)


if __name__ == "__main__":
    unittest.main()
