import copy

from storage.scheme import ArticleData
from ai.processor import normalize_body


def ai_manager(data_list: list[ArticleData]) -> list:
    ai_data_list = copy.deepcopy(data_list)

    for ai_data in ai_data_list:
        ai_data["body"] = normalize_body(ai_data["body"])
