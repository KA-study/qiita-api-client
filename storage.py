from datetime import datetime
import json


def load_data() -> dict:
    try:
        with open("data_storage/qiita_history.json", "r", encoding="utf-8") as file:
            user_data = json.load(file)
        return user_data
    except FileNotFoundError:
        return {}


def save_data(user_data: dict) -> None:

    with open("data_storage/qiita_history.json", "w", encoding="utf-8") as file:
        json.dump(user_data, file, ensure_ascii=False, indent=2)


def manage_params(params: tuple, data: dict, now: str) -> dict:
    key, value = params

    if value is None or value == "":
        return data

    if key not in data:
        data[key] = {}

    if value not in data[key]:
        data[key][value] = {"count": 0, "last_used": None}

    data[key][value]["count"] += 1
    data[key][value]["last_used"] = now

    return data


def update_date(tag: str, keyword: str, sort: str) -> None:
    data = load_data()

    now = datetime.now().isoformat()

    data = manage_params(("tags", tag), data, now)
    data = manage_params(("keywords", keyword), data, now)
    data = manage_params(("sort_options", sort), data, now)

    save_data(data)
