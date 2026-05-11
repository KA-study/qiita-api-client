from typing import TypedDict, Dict
from enum import Enum


class SortOption(Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    LIKES = "likes"
    STOCKS = "stocks"
    TITLE_LENGTH = "title_length"
    TAG_COUNT = "tag_count"

    ORIGINAL = "original"


SORT_MAP = {
    "created_at": SortOption.CREATED_AT,
    "created": SortOption.CREATED_AT,
    "updated_at": SortOption.UPDATED_AT,
    "updated": SortOption.UPDATED_AT,
    "likes": SortOption.LIKES,
    "stocks": SortOption.STOCKS,
    "title_length": SortOption.TITLE_LENGTH,
    "tag_count": SortOption.TAG_COUNT,
    "original": SortOption.ORIGINAL,
}


class ArticleAuthor(TypedDict):
    id: str
    name: str


class ArticleData(TypedDict):
    id: str
    title: str
    title_length: int
    url: str
    created_at: str
    updated_at: str
    author: ArticleAuthor
    tags: list[str]
    tag_count: int
    likes: int
    stocks: int
    body: str


class ActivityItem(TypedDict):
    count: int
    last_used: str  # ISO形式のdatetime文字列


ActivityMap = Dict[str, ActivityItem]
ActivityMapSort = Dict[SortOption, ActivityItem]


class ActivityData(TypedDict):
    tags: ActivityMap
    keywords: ActivityMap
    sort_options: ActivityMapSort


class SerializedActivityData(TypedDict):
    tags: ActivityMap
    keywords: ActivityMap
    sort_options: ActivityMap
