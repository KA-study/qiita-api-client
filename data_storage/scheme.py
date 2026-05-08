from typing import TypedDict, Dict
from processor import SortOption


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
