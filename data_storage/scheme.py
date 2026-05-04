from typing import TypedDict, Dict


class ActivityItem(TypedDict):
    count: int
    last_used: str  # ISO形式のdatetime文字列


ActivityMap = Dict[str, ActivityItem]


class ActivityData(TypedDict):
    tags: ActivityMap
    keywords: ActivityMap
    sort_options: ActivityMap
