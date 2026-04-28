# filter and sort logic


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
            "metrics": {
                "likes": item["likes_count"],
            },
        }
    except KeyError as ex:
        raise ValueError(f"Invalid item structure: missing {ex}")
