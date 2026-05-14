import copy

from storage.scheme import ArticleData
from ai.definitions import AIArticleData
from ai.processor import normalize_for_ai


def ai_manager(data_list: list[ArticleData]) -> list:
    # 安全のため
    data_list_copy = copy.deepcopy(data_list)

    ai_data_list = []

    for data_copy in data_list_copy:
        ai_data_list.append(normalize_for_ai(data_copy))
