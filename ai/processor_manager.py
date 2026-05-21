from datetime import datetime

from storage.scheme import ArticleData
from ai.definitions import (
    AIArticleData, AIExecutionData, AIProcessedData, COST, AIOutPut,
    AIMetaData, TargetAudienceLevel, REUSE_LIMIT_DAYS
)
from ai.normalizer import normalize_for_ai
from ai.repository import AIRepository
from ai.cost_manager import calc_cost, detect_excess
from ai.cost_repository import CostRepository
from ai.ai_processor import ai_api_processor


#hash_valuesは、今までにAI処理をした記事の本文ハッシュ値リスト
def convert_article_to_execution(ai_data_list: list[AIArticleData], hash_values: list) -> list[AIExecutionData]:

    ai_execution_list: list[AIExecutionData] = [] 

    #ai_articleからai_executionに移す。
    for ai_data in ai_data_list:
        ai_execution_data: AIExecutionData = {
            "data_type": "execution",

            "id": ai_data["id"],
            "title": ai_data["title"],
            "body": ai_data["body"],
            "tags": ai_data["tags"],
            "hash_value": ai_data["hash_value"],

            "reuse": True if ai_data["hash_value"] in hash_values else False
        }

        ai_execution_list.append(ai_execution_data)

    return ai_execution_list


def execution_planner(ai_data_list: list[AIArticleData]) -> list[AIExecutionData]:
    ai_repository = AIRepository()

    try:
        hash_values: list = ai_repository.fetch_one_column_from_processed_table("hash_value")

        ai_execution_list = convert_article_to_execution(ai_data_list, hash_values)

        return ai_execution_list

    finally:
        ai_repository.close()


def make_execution_list(data_list: list[ArticleData]) -> list[AIExecutionData]:

    ai_data_list: list[AIArticleData] = []

    for data in data_list:
        ai_data_list.append(normalize_for_ai(data))

    ai_execution_list: list[AIExecutionData] = execution_planner(ai_data_list)

    return ai_execution_list
    

def elapsed_day(processed_at: str) -> int:
    return (datetime.now() - datetime.fromisoformat(processed_at)).days
   

def dict_to_AIProcessedData(
        execution_data: AIExecutionData,
        summary: str,
        reader_level: str
        ) -> AIProcessedData:

    try: 
        ai_output = AIOutPut(
            summary=summary,
            audience_level=TargetAudienceLevel[reader_level]
        )
    except ValueError:
        raise ValueError(f"Invalid Reader_level: {reader_level}")

    ai_metadata = AIMetaData(
        used_prompt_tokens=0,
        used_completion_tokens=0,
        used_total_tokens=0
    )

    processed_data = AIProcessedData(
        id=execution_data["id"],
        title=execution_data["title"],
        body=execution_data["body"],
        tags=execution_data["tags"],
        hash_value=execution_data["hash_value"],
        ai_output=ai_output,
        ai_metadata=ai_metadata
    )

    return processed_data


def should_reuse_ai_result(
        execution_data: AIExecutionData,
        processed_dict: dict
    ) -> bool:

    return execution_data["reuse"] and elapsed_day(processed_dict["processed_at"]) <= REUSE_LIMIT_DAYS


def process_single_article(
        ai_repository: AIRepository,
        execution_data: AIExecutionData,
        cost_repository: CostRepository
) -> AIProcessedData:


    #hash_value一致でAI処理パス（前回分流用）コースに入る
    if execution_data["reuse"]:
        
        processed_dict: dict = ai_repository.fetch_one_row_from_processed_table(execution_data["id"])

        if elapsed_day(processed_dict["processed_at"]):

            processed_data: AIProcessedData = dict_to_AIProcessedData(
                execution_data,
                processed_dict["summary"],
                processed_dict["reader_level"]
            )

            return processed_data
        

    #現在コスト取得
    current_cost = cost_repository.get_current_state()

    #今から実行予定の記事の予測コスト
    estimated_cost = calc_cost([execution_data])

    #コスト超過しないかの確認
    detect_result = detect_excess(estimated_cost, current_cost) 

    if detect_result.is_excess == COST.OVER_LIMIT: #ここから、AI処理を反映させていない状態で通常の検索結果へと戻るように再設計。
        raise RuntimeError("Luck of cost. The estimation of cost was not enough.")

    #AI処理実行
    processed_data: AIProcessedData = ai_api_processor(execution_data)

    return processed_data


