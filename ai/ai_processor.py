import json

from ai.definitions import AIExecutionData, AIProcessedData
from ai.api_client import call_ai_and_return_raw_json



def get_parameters_from_AIExecutionData(execution_data: AIExecutionData) -> str:
    return json.dumps(
        {
            "title": execution_data["title"],
            "tags": execution_data["tags"],
            "body": execution_data["body"]
        },
        ensure=False
    )


def ai_api_processor(execution_data:AIExecutionData) -> AIProcessedData:

    processed_data_json = call_ai_and_return_raw_json(execution_data)
