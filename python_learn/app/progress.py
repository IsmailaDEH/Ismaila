import json
import os

SAVE_FILE = os.path.join(os.path.dirname(__file__), "..", "progress.json")


def _default() -> dict:
    return {"completed_lessons": [], "scores": {}, "xp": 0}


def load() -> dict:
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key in _default():
                data.setdefault(key, _default()[key])
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return _default()


def save(data: dict):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def mark_lesson_done(lesson_id: str, score: int, max_score: int):
    data = load()
    if lesson_id not in data["completed_lessons"]:
        data["completed_lessons"].append(lesson_id)
        earned = int(10 * score / max_score) if max_score else 0
        data["xp"] = data.get("xp", 0) + earned + 5
    data["scores"][lesson_id] = {"score": score, "max": max_score}
    save(data)


def is_done(lesson_id: str) -> bool:
    return lesson_id in load()["completed_lessons"]


def get_xp() -> int:
    return load().get("xp", 0)


def get_score(lesson_id: str) -> dict | None:
    return load()["scores"].get(lesson_id)


def reset():
    save(_default())
