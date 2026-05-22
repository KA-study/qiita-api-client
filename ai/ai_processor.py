import json

from ai.definitions import (
    AIExecutionData, AIProcessedData, RawAIResponse, SUMMARY, READER_LEVEL,
    AIOutPut, AIMetaData)
from ai.api_client import AIAPIClient, MockAIAPIClient



def get_parameters_from_AIExecutionData(execution_data: AIExecutionData) -> str:
    return json.dumps(
        {
            "title": execution_data["title"],
            "tags": execution_data["tags"],
            "body": execution_data["body"]
        },
        ensure_ascii=False
    )

def make_processed_data(raw_data: RawAIResponse, execution_data: AIExecutionData) -> AIProcessedData:

    if set(raw_data.output.keys()) != {SUMMARY, READER_LEVEL}: 
        raise ValueError("required data was not returned by openai.")


    output = AIOutPut(
        summary=raw_data.output[SUMMARY],
        reader_level=raw_data.output[READER_LEVEL]
    )

    meta_data = AIMetaData(
        used_prompt_tokens=raw_data.metadata["prompt_tokens"],
        used_completion_tokens=raw_data.metadata["completion_tokens"],
        used_total_tokens=raw_data.metadata["total_tokens"]
    )

    ai_processed_data = AIProcessedData(
        id=execution_data["id"],
        title=execution_data["title"],
        body=execution_data["body"],
        tags=execution_data["tags"],
        hash_value=execution_data["hash_value"],

        ai_output=output,
        ai_metadata=meta_data
    )    

    return ai_processed_data


#mockと実機能の差し替えは手動。
def ai_api_processor(execution_data: AIExecutionData) -> AIProcessedData:
    #ai_api_client = AIAPIClient()
    mock_ai_api_client = MockAIAPIClient()

    article_data: str = get_parameters_from_AIExecutionData(execution_data)
    #processed_data_json: RawAIResponse = ai_api_client.call_ai(article_data)
    processed_data_json: RawAIResponse = mock_ai_api_client.call_ai(article_data)

    ai_processed_data: AIProcessedData = make_processed_data(processed_data_json, execution_data)

    return ai_processed_data
