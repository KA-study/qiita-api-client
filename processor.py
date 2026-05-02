# filter and sort logic
from enum import Enum
from datetime import datetime


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
            "tag_count": len(item["tags"]),
            "likes": item["likes_count"],
            "stocks": item["stocks_count"],
        }
    except KeyError as ex:
        raise ValueError(f"Invalid item structure: missing {ex}")


class SortOption(Enum):
    # lambda式のxに渡されるのは、正規化後の各記事のメタデータ（辞書型）
    # (sort_key, revrese)
    # lambdaは拡張時に問題となりうる。外部に関数を作り、それで代用するように修正。
    CREATED_AT = (
        lambda x: datetime.fromisoformat(x["created_at"]),
        True,
    )
    UPDATED_AT = (lambda x: datetime.fromisoformat(x["updated_at"]), True)
    LIKES = (lambda x: x["likes"], True)
    STOCKS = (lambda x: x["stocks"], True)
    TITEL_LENGTH = (lambda x: x["title_length"], True)
    TAG_COUNT = (lambda x: x["tag_count"], True)

    def __init__(self, sort_key, reverse: bool):
        self.__sort_key = sort_key
        self.__reverse = reverse

    @property
    def sort_key(self):
        return self.__sort_key

    @property
    def reverse(self):
        return self.__reverse


SORT_MAP = {
    "created_at": SortOption.CREATED_AT,
    "created": SortOption.CREATED_AT,
    "updated_at": SortOption.UPDATED_AT,
    "updated": SortOption.UPDATED_AT,
    "likes": SortOption.LIKES,
    "stocks": SortOption.STOCKS,
    "title_length": SortOption.TITEL_LENGTH,
    "tag_count": SortOption.TAG_COUNT,
}


# 開発者メモ: except節の構造がよくわかっていない
def parse_sort_option(sort_key: str) -> SortOption:
    try:
        return SORT_MAP[sort_key]
    except KeyError as ex:
        raise ValueError(
            f"Invalid sort option: {sort_key}. Available: {list(SORT_MAP)}"
        ) from ex


def sort_data(data: list, sort_key: SortOption) -> list:
    return sorted(data, key=sort_key.sort_key, reverse=sort_key.reverse)
