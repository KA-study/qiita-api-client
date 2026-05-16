import copy

from storage.scheme import ArticleData
from ai.definitions import (
    AIExecutionData, AIProcessedData, COST, EXCESS_RESULT)
from ai.processor_manager import make_execution_list, process_single_article
from ai.cost_manager import first_cost_saver
from ai.cost_repository import CostRepository


def ai_manager(data_list: list[ArticleData]) -> (list[AIProcessedData], EXCESS_RESULT):
    # 安全のため
    data_list_copy = copy.deepcopy(data_list)

    ai_execution_list: list[AIExecutionData] = make_execution_list(data_list_copy) 

    first_cost_result: EXCESS_RESULT = first_cost_saver(ai_execution_list)

    #コスト超過したかに合わせて処理を進める。
    if first_cost_result.is_excess == COST.OVER_LIMIT:
        return (ai_execution_list, first_cost_result)

    processed_list: list[AIProcessedData] = []

    cost_repository = CostRepository()

    for execution_data in ai_execution_list:

        #現在コスト取得
        current_cost = cost_repository.get_current_state()

        #今から実行予定の記事の予測コスト
        estimated_cost = calc_cost([execution_data])

        #コスト超過しないかの確認
        detect_result = detect_excess(estimated_cost, current_cost) 

        if detect_result.is_excess == COST.OVER_LIMIT: #ここから、AI処理を反映させていない状態で通常の検索結果へと戻るように再設計。
            raise RuntimeError("Ruck of cost. The estimation of cost was not enough.")

        #AI処理実行