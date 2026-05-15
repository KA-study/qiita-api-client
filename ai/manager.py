import copy

from storage.scheme import ArticleData
from ai.definitions import AIExecutionData, AIProcessedData
from ai.processor_manager import process_manager
from ai.cost_manager import first_cost_saver


def ai_manager(data_list: list[ArticleData]) -> list[AIProcessedData]:
    # 安全のため
    data_list_copy = copy.deepcopy(data_list)

    ai_execution_list: list[AIExecutionData] = process_manager(data_list_copy) 

    first_cost_saver(ai_execution_list)