from datetime import datetime
import json
import re

from data_storage.scheme import ActivityData
from config import STOPWORDS


def load_data() -> ActivityData:
    try:
        with open("data_storage/qiita_history.json", "r", encoding="utf-8") as file:
            user_data = json.load(file)
        return user_data
    except FileNotFoundError:
        return {}  # type: ignore[return-value]


def save_data(user_data: ActivityData) -> None:

    with open("data_storage/qiita_history.json", "w", encoding="utf-8") as file:
        json.dump(user_data, file, ensure_ascii=False, indent=2)


def manage_params(params: tuple, data: ActivityData, now: str) -> ActivityData:
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


def tokenize(keyword: str) -> list[str]:
    ptn = re.compile(r"[a-zA-Z0-9]+|[ァ-ンー]+|[一-龥]+|[ぁ-ん]+")

    tokens = ptn.findall(keyword)

    tokens = [t() for t in tokens if t not in STOPWORDS and len(t) > 1]

    return tokens


# sort: SortOption.sort_key ("created_at"とか。)
def update_data(tag: str, keyword: str, sort: str) -> ActivityData:
    data = load_data()

    # 保存時はすべて小文字に。破壊的変更を避ける。この関数に他の変数の値を変える責務はない。
    normalized_tag = tag.lower()
    normalized_keyword = keyword.lower()

    now = datetime.now().isoformat()

    data = manage_params(("tags", normalized_tag), data, now)
    data = manage_params(("sort_options", sort), data, now)

    tokens = tokenize(normalized_keyword)

    for token in tokens:
        data = manage_params(("keywords", token), data, now)

    save_data(data)

    return data
