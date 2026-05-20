from typing import TypedDict, Literal, NamedTuple
from dataclasses import dataclass
from enum import StrEnum, Enum
from pathlib import Path
from openai.types.chat import ChatCompletionToolParam

# このLiteralにふくまれる文字列はCREATE_AI_PROCESSED_TABLEの列項目であるが、スペルミスが極めて起こりやすいため、
# AIArticleDataをEnum型継承にするなどして、対応すること。
TABLE_COLUMN_ITEM = Literal[
    "title", "body", "hash_value", "tags", "summary", "audience_level"
]

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
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class AIOutPut:
    summary: str
    audience_level: TargetAudienceLevel


@dataclass
class AIMetaData:
    used_prompt_tokens: float
    used_completion_tokens: float
    used_total_tokens: float


@dataclass
class AIProcessedData:
    # 記事データ
    id: str
    title: str
    body: str
    tags: list[str]
    hash_value: str

    # 処理後データ
    ai_output: AIOutPut
    ai_metadata: AIMetaData


#========以下、AI API関連===============================
AUDIENCE_LEVEL = "audience_level"
SUMMARY = "summary"

TOOLS: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "analyze_article",
            "description": "Summarize the given text and classify reader level",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Japanese summary of the article. Must be within 350 characters."
                    },
                    "audience_level": {
                        "type": "string",
                        "enum": ["beginner", "intermediate", "advanced"],
                        "description": "Estimated reader level of the article"
                    }
                },
                "required": [SUMMARY, AUDIENCE_LEVEL],
                "additionalProperties": False
            }
        }
    }
]

system_prompt = """
You are an article analysis AI.

You must always use the function "analyze_article" to return results.

Constraints:
- summary must be written in Japanese
- summary must be 350 characters or less
- audience_level must be one of:
  - beginner
  - intermediate
  - advanced
- Do not output anything except the function call.
"""


class RawAIResponse(NamedTuple):
    output: dict
    metadata: dict


#========以下、cost_manager関連、編集時は十分注意==========
MAX_COMPLETION_TOKENS = 300
DB_PATH = Path("ai/cost.db")


#今後追加予定
EVENT_TYPE = "add"

CREATE_COST_LOG_TABLE = """
CREATE TABLE IF NOT EXISTS cost_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    article_id TEXT NOT NULL,
    created_at TEXT NOT NULL,

    event_type TEXT NOT NULL,

    prompt_tokens INTEGER NOT NULL,
    completion_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,

    note TEXT
)
"""

CREATE_COST_STATE_TABLE = """
CREATE TABLE IF NOT EXISTS cost_state (
    scope TEXT PRIMARY KEY,

    available_tokens INTEGER NOT NULL,
    used_tokens INTEGER NOT NULL,
    last_log_id: TEXT NOT NULL,

    updated_at TEXT NOT NULL
)
"""

CREATE_AI_PROCESSED_DATA_TABLE = """
CREATE TABLE IF NOT EXISTS ai_processed_data (
    article_id INTEGER PRIMARY KEY,

    body_hash TEXT NOT NULL UNIQUE,

    summary TEXT NOT NULL,

    reader_level TEXT NOT NULL,

    model_name TEXT NOT NULL,

    prompt_version TEXT NOT NULL,

    created_at TEXT NOT NULL,

    updated_at TEXT NOT NULL
)
"""

CREATE_AI_PROCESSED_HASH_INDEX = """
CREATE INDEX IF NOT EXISTS idx_ai_processed_hash
ON ai_processed_data(body_hash)"""


class COST(Enum):
    OVER_LIMIT = "over_limit" 
    WITHIN_LIMIT = "within_limit"


@dataclass(slots=True)
class EXCESS_RESULT:
    is_excess: COST

    estimated_cost: float
    available_cost: float

    remaining_cost: float


@dataclass(slots=True)
class ESTIMATED_COST:
    estimated_cost: float = 0

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

@dataclass
class AI_MODEL_INFO:
    name: str

    prompt_cost_per_token: float
    completion_cost_per_token: float

AI_MODEL = AI_MODEL_INFO(
    name="gpt-4o-mini",
    prompt_cost_per_token=0.15 / 1_000_000,
    completion_cost_per_token=0.6 / 1_000_000
)

@dataclass
class COST_STATE:
    scope: str

    available_tokens: int
    used_tokens: int
    last_log_id: str

    updated_at: str