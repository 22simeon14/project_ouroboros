import json
from pathlib import Path


def load_best_score(save_path):
    path = Path(save_path)
    if not path.exists():
        return 0

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError, TypeError):
        return 0

    if not isinstance(data, dict):
        return 0

    best_score = data.get("best_score", 0)
    if not isinstance(best_score, int) or best_score < 0:
        return 0

    return best_score


def update_best_score(save_path, current_score):
    path = Path(save_path)
    best_score = load_best_score(path)

    if current_score > best_score:
        best_score = current_score
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump({"best_score": best_score}, file, indent=2)

    return best_score
