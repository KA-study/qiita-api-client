from typing import TypedDict


class ActivityItem(TypedDict):
    count: int
    last_used: str  # ISO形式のdatetime文字列


class ActivityData(TypedDict):
    tags: ActivityItem
    keywords: ActivityItem
    sort_options: ActivityItem
