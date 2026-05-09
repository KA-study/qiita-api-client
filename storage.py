from datetime import datetime
import json
from json import JSONDecodeError
import re

from data_storage.scheme import (
    ActivityData,
    ActivityMapSort,
    ActivityItem,
    SerializedActivityData,
    SortOption,
    SORT_MAP,
)
from config import STOPWORDS


def normalize_sort_options(sort_options: dict[str, ActivityItem]) -> ActivityMapSort:

    return {SORT_MAP[sort_option]: value for sort_option, value in sort_options.items()}


def serialize_sort_options(sort_options: ActivityMapSort) -> dict[str, ActivityItem]:

    return {sort_option.value: value for sort_option, value in sort_options.items()}


def load_data() -> ActivityData:
    try:
        with open("data_storage/qiita_history.json", "r", encoding="utf-8") as file:
            user_data = json.load(file)

            # SortOption型にデータ変換
            user_data["sort_options"] = normalize_sort_options(
                user_data["sort_options"]
            )

            return user_data

    except (FileNotFoundError, JSONDecodeError):
        return {}  # type: ignore[return-value]


def save_data(user_data: ActivityData) -> None:

    user_data_serialized: SerializedActivityData = {
        "tags": {},
        "keywords": {},
        "sort_options": {},
    }

    if user_data["tags"]:
        user_data_serialized["tags"] = user_data["tags"]

    if user_data["keywords"]:
        user_data_serialized["keywords"] = user_data["keywords"]

    if user_data["sort_options"]:
        user_data_serialized["sort_options"] = serialize_sort_options(
            user_data["sort_options"]
        )

    with open("data_storage/qiita_history.json", "w", encoding="utf-8") as file:
        json.dump(user_data_serialized, file, ensure_ascii=False, indent=2)


def manage_params(
    params: tuple[str, str | SortOption], data: ActivityData, now: str
) -> ActivityData:
    key, value = params

    if not value:
        return data

    if value not in data[key]:
        data[key][value] = {"count": 0, "last_used": None}

    data[key][value]["count"] += 1
    data[key][value]["last_used"] = now

    return data


def tokenize(keyword: str) -> list[str]:
    ptn = re.compile(r"[a-zA-Z0-9]+|[ァ-ンー]+|[一-龥]+|[ぁ-ん]+")

    tokens = ptn.findall(keyword)

    tokens = [t.lower() for t in tokens if t not in STOPWORDS and len(t) > 1]

    return tokens


# sort: SortOption.sort_key ("created_at"とか。)
def update_data(tag: str, keyword: str, sort: SortOption) -> ActivityData:
    data = load_data()

    # 保存時はすべて小文字に。破壊的変更を避ける。この関数に他の変数の値を変える責務はない。
    normalized_tag = tag.lower()
    normalized_keyword = keyword.lower()

    now = datetime.now().isoformat()

    data.setdefault("tags", {})
    data.setdefault("keywords", {})
    data.setdefault("sort_options", {})

    data = manage_params(("tags", normalized_tag), data, now)
    data = manage_params(("sort_options", sort), data, now)

    tokens = tokenize(normalized_keyword)

    for token in tokens:
        data = manage_params(("keywords", token), data, now)

    save_data(data)

    return data
