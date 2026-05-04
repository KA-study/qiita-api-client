# filter and sort logic
from enum import Enum
from datetime import datetime

from data_storage.scheme import ActivityData
from score import calc_score_closure


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
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    LIKES = "likes"
    STOCKS = "stocks"
    TITEL_LENGTH = "title_length"
    TAG_COUNT = "tag_count"

    ORIGINAL = "original"

    def __init__(self, sort_key):
        self.__sort_key = sort_key

    @property
    def sort_key(self):
        return self.__sort_key


SORT_MAP = {
    "created_at": SortOption.CREATED_AT,
    "created": SortOption.CREATED_AT,
    "updated_at": SortOption.UPDATED_AT,
    "updated": SortOption.UPDATED_AT,
    "likes": SortOption.LIKES,
    "stocks": SortOption.STOCKS,
    "title_length": SortOption.TITEL_LENGTH,
    "tag_count": SortOption.TAG_COUNT,
    "original": SortOption.ORIGINAL,
}

SORT_LOGIC = {
    # dataの要素がｘである。すなわち、各記事の辞書がｘである。
    SortOption.CREATED_AT: lambda x: datetime.fromisoformat(x["created_at"]),
    SortOption.UPDATED_AT: lambda x: datetime.fromisoformat(x["updated_at"]),
    SortOption.LIKES: lambda x: x["likes"],
    SortOption.STOCKS: lambda x: x["stocks"],
    SortOption.TITEL_LENGTH: lambda x: x["title_length"],
    SortOption.TAG_COUNT: lambda x: x["tag_count"],
}


def sort_data(logs: ActivityData, data: list, sort_key: SortOption) -> list:

    if sort_key is not SortOption.ORIGINAL:
        sort_logic = SORT_LOGIC[sort_key]
        # key=sortkey の sort_keyはSORT_MAPのいずれかのvalue、つまり文字列。
        return sorted(
            data, key=sort_logic, reverse=True
        )  # reverseのことはおいおい考える
    else:
        calc_article_score = calc_score_closure()

        return sorted(
            data,
            key=lambda x: calc_article_score(logs, x, sort_key.sort_key),
            reverse=True,  # reverseは後ほど改善すること。
        )
