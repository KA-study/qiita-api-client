#manage almost all except for definition, about AI API cost. Be careful when you edit this file.
import tiktoken

from ai.definitions import (
    AIExecutionData, ESTIMATED_COST, AI_MODEL,
    MAX_COMPLETION_TOKENS, COST_STATE, EXCESS_RESULT,
    COST)
from ai.cost_repository import CostRepository


def get_encoding(model: str):
    return tiktoken.encoding_for_model(model)

def count_tokens(text: str, model: str) -> int:
    encoding = get_encoding(model)
    return len(encoding.encode(text))


#total_costを保存して取り出す必要がある。DB操作が必要だと思われる。後ほど追加。
def calc_cost(
    ai_execution_list: list[AIExecutionData]
) -> ESTIMATED_COST:

    prompt_tokens = 0
    completion_tokens = 0

    for data in ai_execution_list:
        prompt_tokens += count_tokens(data["title"], AI_MODEL.name)
        prompt_tokens += count_tokens(data["body"], AI_MODEL.name)

        completion_tokens += MAX_COMPLETION_TOKENS

    total_tokens = prompt_tokens + completion_tokens

    estimated_cost = (
        prompt_tokens * AI_MODEL.prompt_cost_per_token
        + completion_tokens * AI_MODEL.completion_cost_per_token
    )

    return ESTIMATED_COST(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        estimated_cost=estimated_cost,
    )


def detect_excess(estimated: ESTIMATED_COST, current: COST_STATE) -> EXCESS_RESULT:
    remaining_cost = (
        current.available_cost
        - estimated.estimated_cost
    )

    return EXCESS_RESULT(
        is_excess=COST.OVER_LIMIT if remaining_cost < 0 else COST.WITHIN_LIMIT,
        estimated_cost=estimated.estimated_cost,
        available_cost=current.available_cost,
        remaining_cost=remaining_cost
    )


#一回目のコスト管理処理の親関数
def first_cost_saver(api_execution_list: list[AIExecutionData]) -> EXCESS_RESULT:
    estimated_cost: ESTIMATED_COST = calc_cost(api_execution_list) 

    cost_repository = CostRepository()

    current_cost: COST_STATE = cost_repository.get_current_state()

    excess_result: EXCESS_RESULT = detect_excess(estimated_cost, current_cost)

    return excess_result