import copy

from storage.scheme import ArticleData
from ai.processor import normalize_for_ai


def ai_manager(data_list: list[ArticleData]) -> list:
    # 安全のため
    ai_data_list = copy.deepcopy(data_list)

    for ai_data in ai_data_list:
        ai_data = normalize_for_ai(ai_data)
