#manage almost all except for definition, about AI API cost. Be careful when you edit this file.
import tiktoken
from functools import cache

from ai.definitions import (
    AIExecutionData, ESTIMATED_COST, AI_MODEL,
    MAX_OUTPUT_TOKENS, COST_STATE, EXCESS_RESULT,
    COST)
from ai.cost_repository import CostRepository


def get_encoding(model: str):
    return tiktoken.encoding_for_model(model)

def count_tokens(text: str, model: str) -> int:
    encoding = get_encoding(model)
    return len(encoding.encode(text))


#total_costを保存して取り出す必要がある。DB操作が必要だと思われる。後ほど追加。
def first_costs_calc(
    ai_execution_list: list[AIExecutionData]
) -> ESTIMATED_COST:

    input_tokens = 0
    output_tokens = 0

    for data in ai_execution_list:
        input_tokens += count_tokens(data["title"], AI_MODEL.name)
        input_tokens += count_tokens(data["body"], AI_MODEL.name)

        output_tokens += MAX_OUTPUT_TOKENS

    total_tokens = input_tokens + output_tokens

    estimated_cost = (
        input_tokens * AI_MODEL.input_cost_per_token
        + output_tokens * AI_MODEL.output_cost_per_token
    )

    return ESTIMATED_COST(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
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
def first_cost_saver(api_execution_list: list[AIExecutionData]) -> None:
    estimated_cost: ESTIMATED_COST = first_costs_calc(api_execution_list) 

    cost_repository = CostRepository()

    current_cost: COST_STATE = cost_repository.get_current_state()

    detect_excess(estimated_cost, current_cost)