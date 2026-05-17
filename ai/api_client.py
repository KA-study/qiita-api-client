from openai import OpenAI
from openai.types.chat import ChatCompletionMessageToolCall
import json
from dotenv import load_dotenv
import os
from typing import cast

from ai.definitions import (
    AIExecutionData, TOOLS, AI_MODEL, system_prompt
    )
from ai.ai_processor import get_parameters_from_AIExecutionData


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_ai_and_return_raw_json(execution_data: AIExecutionData):

    response = client.chat.completions.create(
        model=AI_MODEL.name,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": get_parameters_from_AIExecutionData(execution_data)
            }
        ],
        tools=TOOLS,
        tool_choice={
            "type": "function",
            "function": {"name": "analyze_article"}
        }
    )

    if response.choices[0].message.tool_calls is None:
        raise ValueError("No tool calls in response")
    
    #castの意味は分からないが、AIにエラーを直すように指示すると、こうなった。
    tool_call = cast(
        ChatCompletionMessageToolCall,
        response.choices[0].message.tool_calls[0]
        )

    raw_json = json.loads(tool_call.function.arguments)

    return raw_json