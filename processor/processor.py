# filter and sort logic
from datetime import datetime

from storage.scheme import ActivityData, SortOption, ArticleData
from processor.score import calc_article_score


def normalize(item: dict) -> ArticleData:
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
            "body": item["body"],

            "ai_processed_data": None
        }
    except KeyError as ex:
        raise ValueError(f"Invalid item structure: missing {ex}")


SORT_LOGIC = {
    # dataの要素がｘである。すなわち、各記事の辞書がｘである。
    SortOption.CREATED_AT: lambda x: datetime.fromisoformat(x["created_at"]),
    SortOption.UPDATED_AT: lambda x: datetime.fromisoformat(x["updated_at"]),
    SortOption.LIKES: lambda x: x["likes"],
    SortOption.STOCKS: lambda x: x["stocks"],
    SortOption.TITLE_LENGTH: lambda x: x["title_length"],
    SortOption.TAG_COUNT: lambda x: x["tag_count"],
}


def sort_data(
    logs: ActivityData, data: list[ArticleData], sort_key: SortOption
) -> list:

    now = datetime.now()

    if sort_key is not SortOption.ORIGINAL:
        sort_logic = SORT_LOGIC[sort_key]
        # key=sortkey の sort_keyはSORT_MAPのいずれかのvalue、つまり文字列。
        return sorted(
            data, key=sort_logic, reverse=True
        )  # reverseのことはおいおい考える
    else:
        return sorted(
            data,
            key=lambda x: calc_article_score(logs, x, now),
            reverse=True,  # reverseは後ほど改善すること。
        )
