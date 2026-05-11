from typing import TypedDict


class AIArticleData(TypedDict):
    id: str
    title: str
    body: str
    tags: list[str]
