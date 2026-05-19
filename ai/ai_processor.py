import json

from ai.definitions import (
    AIExecutionData, AIProcessedData, RawAIResponse, SUMMARY, AUDIENCE_LEVEL,
    AIOutPut, AIMetaData)
from ai.api_client import AIAPIClient



def get_parameters_from_AIExecutionData(execution_data: AIExecutionData) -> str:
    return json.dumps(
        {
            "title": execution_data["title"],
            "tags": execution_data["tags"],
            "body": execution_data["body"]
        },
        ensure=False
    )

def make_processed_data(raw_data: RawAIResponse, execution_data: AIExecutionData) -> AIProcessedData:

    if set(raw_data.output.keys()) == {SUMMARY, AUDIENCE_LEVEL}: 
        raise ValueError("required data was not returned by openai.")


    output = AIOutPut(
        summary=raw_data.output[SUMMARY],
        audience_level=raw_data.output[AUDIENCE_LEVEL]
    )

    meta_data = AIMetaData(
        used_input_tokens=raw_data.metadata["input_tokens"],
        used_output_tokens=raw_data.metadata["output_tokens"],
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


def ai_api_processor(execution_data: AIExecutionData) -> AIProcessedData:
    ai_api_client = AIAPIClient()

    processed_data_json: RawAIResponse = ai_api_client.call_ai(execution_data)

    ai_processed_data: AIProcessedData = make_processed_data(processed_data_json, execution_data)

    return ai_processed_data
