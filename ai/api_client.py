from openai import OpenAI
from openai.types.chat import ChatCompletionMessageToolCall
from openai.types.chat.chat_completion import ChatCompletion
import json
from dotenv import load_dotenv
import os
from typing import cast

from ai.definitions import (
    TOOLS, AI_MODEL, system_prompt, RawAIResponse
    )


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
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
    
        return (raw_ai_output, raw_ai_metadata)
    

    def call_ai(self, article_data: str) -> RawAIResponse:

        response = self.client.chat.completions.create(
            model=AI_MODEL.name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": article_data
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


#デバッグ時差し替え用
class MockAIAPIClient:

    def call_ai(self, article_data: str) -> RawAIResponse:

        mock_output = {
            "summary": (
                "これはモック環境で生成された要約です。"
                "実際のOpenAI APIは呼び出していません。"
            ),
            "reader_level": TargetReaderLevel.BEGINNER.value
        }

        mock_metadata = {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150
        }

        return RawAIResponse(
            output=mock_output,
            metadata=mock_metadata
        )