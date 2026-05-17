from typing import TypedDict, Literal
from dataclasses import dataclass
from enum import StrEnum, Enum
from pathlib import Path
from openai.types.chat import ChatCompletionToolParam

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
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class AIProcessedData:
    # 記事データ
    id: str
    title: str
    body: str
    tags: list[str]
    hash_value: str

    # 処理後データ
    summary: str
    audiencelevel: TargetAudienceLevel

    used_input_tokens: float
    used_output_tokens: float


#========以下、AI API関連===============================
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
                "required": ["summary", "audience_level"],
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


#========以下、cost_manager関連、編集時は十分注意==========
MAX_OUTPUT_TOKENS = 300
DB_PATH = Path("ai/cost.db")


CREATE_COST_LOG_TABLE = """
CREATE TABLE IF NOT EXISTS cost_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    created_at TEXT NOT NULL,

    execution_id TEXT NOT NULL,

    event_type TEXT NOT NULL,

    delta_cost INTEGER NOT NULL,

    note TEXT
)
"""

CREATE_COST_STATE_TABLE = """
CREATE TABLE IF NOT EXISTS cost_state (
    scope TEXT PRIMARY KEY,

    available_cost INTEGER NOT NULL,

    reserved_cost INTEGER NOT NULL,

    committed_cost INTEGER NOT NULL,

    updated_at TEXT NOT NULL
)
"""


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

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

@dataclass
class AI_MODEL_INFO:
    name: str

    input_cost_per_token: float
    output_cost_per_token: float

AI_MODEL = AI_MODEL_INFO(
    name="gpt-4o-mini",
    input_cost_per_token=0.15 / 1_000_000,
    output_cost_per_token=0.6 / 1_000_000
)

@dataclass
class COST_STATE:
    scope: str

    available_cost: int
    reserved_cost: int
    committed_cost: int

    updated_at: str