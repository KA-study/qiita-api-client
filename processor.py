# filter and sort logic
import argparse
from datetime import datetime

from config import SortOption


def normalize(item: dict) -> dict:
    # Qiita API response を内部で扱う共通フォーマットに整形
    try:
        return {
            "id": item["id"],
            "title": item["title"],
            "url": item["url"],
            "created_at": item["created_at"],
            "updated_at": item["updated_at"],
            "author": {
                "id": item["user"]["id"],
                "name": item["user"]["name"],
            },
            "tags": [tag["name"] for tag in item["tags"]],
            "likes": item["likes_count"],
        }
    except KeyError as ex:
        raise ValueError(f"Invalid item structure: missing {ex}")


def sort_data(data: list, args_sort: SortOption) -> list:
    # argsは、mainのほうで.sortを付与している。

    match args_sort:
        case SortOption.CREATED_AT | SortOption.UPDATED_AT:
            key = args_sort.value[0]
            return sorted(data, key=lambda x: datetime.fromisoformat(x[key]))
        case SortOption.LIKES:
            return sorted(data, key=lambda x: x["likes"], reverse=True)

    raise ValueError("sorting process failed.")
