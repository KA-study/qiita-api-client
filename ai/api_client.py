from openai import OpenAI
from openai.types.chat import ChatCompletionMessageToolCall
from openai.types.chat.chat_completion import ChatCompletion
import json
from dotenv import load_dotenv
import os
from typing import cast

from ai.definitions import (
    AIExecutionData, TOOLS, AI_MODEL, system_prompt, RawAIResponse
    )
from ai.ai_processor import get_parameters_from_AIExecutionData


class AIAPIClient:

    def __init__(self):
        load_dotenv()
        self.__client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    @property
    def client(self):
        return self.__client


    def openai_to_json(self, response: ChatCompletion) -> tuple[dict, dict]:

        if response.choices[0].message.tool_calls is None:
            raise ValueError("No tool calls in response")
      
        #castの意味は分からないが、AIにエラーを直すように指示すると、こうなった。
        tool_call = cast(
            ChatCompletionMessageToolCall,
            response.choices[0].message.tool_calls[0]
            )

        raw_ai_output = json.loads(tool_call.function.arguments)


        if not response.usage:
            raise ValueError("No metadata was returned by openai api.")

       #metadataをdict/listなどの基本型に落とし込む 
        raw_ai_metadata = {
            "input_tokens": response.usage.prompt_tokens,
            "ouput_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
    
        return (raw_ai_output, raw_ai_metadata)
    

    def call_ai(self, execution_data: AIExecutionData) -> RawAIResponse:

        response = self.client.chat.completions.create(
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

        raw_ai_output, raw_ai_metadata = self.openai_to_json(response)

        return RawAIResponse(
            output=raw_ai_output,
            metadata=raw_ai_metadata
        )
    