import json
import tempfile
import unittest
from pathlib import Path

from level import load_level


VALID_LEVEL = {
    "name": "Test Chamber",
    "start": [2, 3],
    "walls": [[5, 5], [6, 6]],
    "exit": [10, 10],
    "energy_goal": 3,
}


class TestLoadLevel(unittest.TestCase):
    def _write_temp_level(self, data):
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump(data, temp_file)
        temp_file.close()
        return Path(temp_file.name)

    def test_valid_json_loads_successfully(self):
        path = self._write_temp_level(VALID_LEVEL)
        try:
            level = load_level(path)
            self.assertIsNotNone(level)
        finally:
            path.unlink()

    def test_valid_level_with_exit_and_energy_goal_loads_successfully(self):
        path = self._write_temp_level(VALID_LEVEL)
        try:
            level = load_level(path)
            self.assertEqual(level.exit, (10, 10))
            self.assertEqual(level.energy_goal, 3)
        finally:
            path.unlink()

    def test_loaded_level_has_correct_name_and_start(self):
        path = self._write_temp_level(VALID_LEVEL)
        try:
            level = load_level(path)
            self.assertEqual(level.name, "Test Chamber")
            self.assertEqual(level.start, (2, 3))
        finally:
            path.unlink()

    def test_walls_are_converted_to_set_of_tuples(self):
        path = self._write_temp_level(
            {
                **VALID_LEVEL,
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

    def test_missing_exit_raises_value_error(self):
        data = {key: value for key, value in VALID_LEVEL.items() if key != "exit"}
        path = self._write_temp_level(data)
        try:
            with self.assertRaises(ValueError):
                load_level(path)
        finally:
            path.unlink()

    def test_missing_energy_goal_raises_value_error(self):
        data = {key: value for key, value in VALID_LEVEL.items() if key != "energy_goal"}
        path = self._write_temp_level(data)
        try:
            with self.assertRaises(ValueError):
                load_level(path)
        finally:
            path.unlink()

    def test_invalid_start_type_raises_value_error(self):
        path = self._write_temp_level(
            {
                **VALID_LEVEL,
                "start": "bad",
            }
        )
        try:
            with self.assertRaises(ValueError):
                load_level(path)
        finally:
            path.unlink()

    def test_invalid_exit_raises_value_error(self):
        path = self._write_temp_level(
            {
                **VALID_LEVEL,
                "exit": [1],
            }
        )
        try:
            with self.assertRaises(ValueError):
                load_level(path)
        finally:
            path.unlink()

    def test_invalid_energy_goal_raises_value_error(self):
        for bad_goal in (0, -1, 3.5, "3"):
            path = self._write_temp_level(
                {
                    **VALID_LEVEL,
                    "energy_goal": bad_goal,
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
                **VALID_LEVEL,
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
