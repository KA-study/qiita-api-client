# export csv/json
from datetime import datetime

from storage.scheme import ArticleData


def format_item(item: ArticleData, index: int) -> str:
    if item.get("created_at"):
        return (
            f"[{index}] {item["title"]}\n"
            f"    tags: {item["tags"]}\n"
            f"    likes: {item.get("likes", 0)}\n"
            f"    created_at: {
                datetime.fromisoformat(
                    str(
                        item.get("created_at")
                        )
                    ).strftime(
                        "%Y-%m-%d %H:%M:%S"
                        )
                    }\n"
            f"    url: {item["url"]}\n"
        )
    else:
        raise ValueError(f"the created_at {item["title"]} is unclear")


def output(data: list[ArticleData]) -> None:
    print("\n=======result========\n")

    for i, item in enumerate(data, 1):
        print(format_item(item, i))
