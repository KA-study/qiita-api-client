# filter and sort logic
import argparse
from datetime import datetime


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


def sort_data(data: list, args: argparse.Namespace) -> list:
    sorted_data = []

    match args.sort:
        case "created_at" | "updated_at" as date:
            sorted_data = sorted(data, key=lambda x: datetime.fromisoformat(x[date]))
        case "likes":
            sorted_data = sorted(data, key=lambda x: x["likes"], reverse=True)

    if not sorted_data:
        raise ValueError("sorting process failed.")

    return sorted_data
