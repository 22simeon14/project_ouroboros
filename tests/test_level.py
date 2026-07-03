import json
import tempfile
import unittest
from pathlib import Path

from level import load_level


class TestLoadLevel(unittest.TestCase):
    def _write_temp_level(self, data):
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump(data, temp_file)
        temp_file.close()
        return Path(temp_file.name)

    def test_valid_json_loads_successfully(self):
        path = self._write_temp_level(
            {
                "name": "Test Chamber",
                "start": [2, 3],
                "walls": [[5, 5], [6, 6]],
            }
        )
        try:
            level = load_level(path)
            self.assertIsNotNone(level)
        finally:
            path.unlink()

    def test_loaded_level_has_correct_name_and_start(self):
        path = self._write_temp_level(
            {
                "name": "Test Chamber",
                "start": [2, 3],
                "walls": [[5, 5]],
            }
        )
        try:
            level = load_level(path)
            self.assertEqual(level.name, "Test Chamber")
            self.assertEqual(level.start, (2, 3))
        finally:
            path.unlink()

    def test_walls_are_converted_to_set_of_tuples(self):
        path = self._write_temp_level(
            {
                "name": "Test Chamber",
                "start": [1, 1],
                "walls": [[5, 5], [6, 6], [5, 5]],
            }
        )
        try:
            level = load_level(path)
            self.assertIsInstance(level.walls, set)
            self.assertEqual(level.walls, {(5, 5), (6, 6)})
        finally:
            path.unlink()

    def test_missing_required_key_raises_value_error(self):
        path = self._write_temp_level(
            {
                "name": "Test Chamber",
                "start": [2, 3],
            }
        )
        try:
            with self.assertRaises(ValueError):
                load_level(path)
        finally:
            path.unlink()

    def test_invalid_start_type_raises_value_error(self):
        path = self._write_temp_level(
            {
                "name": "Test Chamber",
                "start": "bad",
                "walls": [],
            }
        )
        try:
            with self.assertRaises(ValueError):
                load_level(path)
        finally:
            path.unlink()

    def test_invalid_walls_type_raises_value_error(self):
        path = self._write_temp_level(
            {
                "name": "Test Chamber",
                "start": [2, 3],
                "walls": "bad",
            }
        )
        try:
            with self.assertRaises(ValueError):
                load_level(path)
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
