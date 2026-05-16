from storage.scheme import ArticleData
from ai.definitions import (
    AIArticleData, AIExecutionData
)
from ai.normalizer import normalize_for_ai
from ai.repository import execution_planner


def make_execution_list(data_list: list[ArticleData]) -> list[AIExecutionData]:

    ai_data_list: list[AIArticleData] = []

    for data in data_list:
        ai_data_list.append(normalize_for_ai(data))

    ai_execution_list: list[AIExecutionData] = execution_planner(ai_data_list)

    return ai_execution_list