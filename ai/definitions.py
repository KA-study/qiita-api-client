from typing import TypedDict, Literal
from enum import StrEnum

# このLiteralにふくまれる文字列はCREATE_AI_PROCESSED_TABLEの列項目であるが、スペルミスが極めて起こりやすいため、
# AIArticleDataをEnum型継承にするなどして、対応すること。
TABLE_COLUMN_ITEM = Literal[
    "title", "body", "hash_value", "tags", "summary", "audience_level"
]


CREATE_AI_PROCESSED_TABLE = """
CREATE TABLE IF NOT EXISTS ai_processed(
    id TEXT PRIMARY KEY,
    
    --記事メタ
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    hash_value TEXT NOT NULL,
    tags TEXT NOT NULL, --JSON文字列に変換しておく。
    
    --AI処理結果
    summary TEXT NOT NULL,
    audience_level TEXT NOT NULL
    )
"""


class AIArticleData(TypedDict):
    data_type: Literal["article"]

    id: str
    title: str
    body: str
    tags: list[str]
    hash_value: str


class AIExecutionData(TypedDict):
    data_type: Literal["execution"]

    id: str
    title: str
    body: str
    tags: list[str]
    hash_value: str  # 本文ハッシュ結果

    reuse: bool


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
    hash_value: str

    # 処理後データ
    summary: str
    audiencelevel: TargetAudienceLevel
