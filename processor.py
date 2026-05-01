# filter and sort logic
from config import SortOption


def normalize(item: dict) -> dict:
    # Qiita API response を内部で扱う共通フォーマットに整形
    try:
        return {
            "id": item["id"],
            "title": item["title"],
            "title_length": len(item["title"]),
            "url": item["url"],
            "created_at": item["created_at"],
            "updated_at": item["updated_at"],
            "author": {
                "id": item["user"]["id"],
                "name": item["user"]["name"],
            },
            # itemの要素のtagsの構造は以下である。
            # "tags": [
            #   {"name": "Python"},
            #   {"name": "FastAPI"},
            # ]
            "tags": [tag["name"] for tag in item["tags"]],
            "tag_count": len(item["title"]),
            "likes": item["likes_count"],
        }
    except KeyError as ex:
        raise ValueError(f"Invalid item structure: missing {ex}")


def sort_data(data: list, args_sort: SortOption) -> list:
    # argsは、mainのほうで.sortを付与している。

    # is_api_supportedがTrueの場合、すでに並び替え済み。
    if not args_sort.value[1]:
        return sorted(data, key=lambda item: item[args_sort.value[0]], reverse=True)

    return data
