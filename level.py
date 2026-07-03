import json


class Level:
    def __init__(self, name, start, walls, exit_coord, energy_goal):
        self.name = name
        self.start = start
        self.walls = walls
        self.exit = exit_coord
        self.energy_goal = energy_goal


def _validate_coordinate(value, key_name):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"'{key_name}' must be a list of two numbers [x, y]")
    if not all(isinstance(n, int) and not isinstance(n, bool) for n in value):
        raise ValueError(f"'{key_name}' must contain integer coordinates")
    return tuple(value)


def _validate_energy_goal(value):
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError("'energy_goal' must be a positive integer")
    return value


def load_level(path):
    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Level file must contain a JSON object")

    for key in ("name", "start", "walls", "exit", "energy_goal"):
        if key not in data:
            raise ValueError(f"Missing required key: '{key}'")

    if not isinstance(data["name"], str):
        raise ValueError("'name' must be a string")

    start = _validate_coordinate(data["start"], "start")
    exit_coord = _validate_coordinate(data["exit"], "exit")
    energy_goal = _validate_energy_goal(data["energy_goal"])

    walls_data = data["walls"]
    if not isinstance(walls_data, list):
        raise ValueError("'walls' must be a list of coordinates")

    walls = set()
    for index, coord in enumerate(walls_data):
        if not isinstance(coord, list) or len(coord) != 2:
            raise ValueError(f"'walls' entry at index {index} must be [x, y]")
        if not all(isinstance(n, int) and not isinstance(n, bool) for n in coord):
            raise ValueError(f"'walls' entry at index {index} must contain integers")
        walls.add(tuple(coord))

    return Level(data["name"], start, walls, exit_coord, energy_goal)
