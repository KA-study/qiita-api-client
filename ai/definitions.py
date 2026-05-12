from typing import TypedDict, Literal
from enum import StrEnum


class AIArticleData(TypedDict):
    data_type: Literal["article"]

    id: str
    title: str
    body: str
    tags: list[str]
    hash_value: str


class AIExecutionData(TypedDict):
    data_type: Literal["excution"]

    id: str
    title: str
    body: str
    tags: list[str]
    hash_value: str  # 本文ハッシュ結果


# StrEnumにすることで、実質的にdictとして扱える。(Enuオブジェクトじゃなくてstrとしてふるまう)
class TargetAudienceLevel(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermidiate"
    ADVANCED = "advanced"


class AIProcessedData(TypedDict):
    # 記事データ
    id: str
    title: str
    body: str
    tags: list[str]
    hash_value: int

    # 処理後データ
    summary: str
    audiencelevel: TargetAudienceLevel
