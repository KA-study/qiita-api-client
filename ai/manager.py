import copy

from storage.scheme import ArticleData
from ai.definitions import AIExecutionData
from ai.processor_manager import normalize_for_ai, DB_main_fetcher
from ai.processor_manager import process_manager
from ai.cost_manager import first_cost_checker


def ai_manager(data_list: list[ArticleData]) -> list:
    # 安全のため
    data_list_copy = copy.deepcopy(data_list)

    ai_execution_list: list[AIExecutionData] = process_manager(data_list_copy) 

    for data_copy in data_list_copy:
        ai_data_list.append(normalize_for_ai(data_copy))
