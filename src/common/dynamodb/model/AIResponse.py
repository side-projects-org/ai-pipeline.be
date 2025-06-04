from typing import Type, Optional, Sequence, Text, Any

from pynamodb.attributes import UnicodeAttribute, MapAttribute, DynamicMapAttribute, NumberAttribute

from common.constants import BaseConfig, ModelType
from common.dynamodb.attributes import Attr

from common.dynamodb.model import MyModel
from common.dynamodb.model.MyModel import _T

"""
AIResponse 모델 예시
{
    "pk": "AIResponse#sample_key",
    "sk": "AIResponse#sample_prompt_name",
    "item_type": "AIResponse",
    
    "key": "sample_key",
    "prompt_name": "sample_prompt_name", # 프롬프트의 이름
    "version": "sample_prompt_name", # 프롬프트의 이름
    "created_at": "2023-10-01T12:00:00Z",
    "used_params": {
        "messages": [
            {
                "role": "user",
                "content": "sample content"
            },
            {
                "role": "assistant",
                "content": "sample content"
            }
        ],
        "max_tokens": 100,
        "model": "gpt-3.5-turbo",
        "response_format": "text",
        "temperature": 0.7,
        "stream": False,
    },
    "response": {
        "id": "sample_response_id",
        "object": "chat.completion",
        "created": 1696156800,
        "model": "gpt-3.5-turbo",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "sample response content"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }
}
"""


class AIResponse(MyModel):
    class Meta:
        table_name = f"{BaseConfig.PROJECT_NAME}_{BaseConfig.STAGE_NAME}_prompt_v2"
        region = BaseConfig.AWS_REGION


    item_type = UnicodeAttribute(null=False, default=ModelType.AIResponse.value)
    prompt_name = UnicodeAttribute(null=False)
    version = UnicodeAttribute(null=False)

    params = Attr.AIRequestParamsAttribute(null=True)

    response = Attr.AIResponseAttribute(null=True)

    @classmethod
    def build_pk(cls, prompt_name: str, **kwargs) -> str:
        return f"{prompt_name}"

    @classmethod
    def build_sk(cls, item_type: str, version: str, key: str, **kwargs) -> str:
        return f"{item_type}#{version}#{key}"

    @classmethod
    def get_item(
        cls,
        prompt_name: str,
        version: str,
        key: str,
        consistent_read: bool = True,
        attributes_to_get: Optional[Sequence[Text]] = None,
        **kwargs: Any
    ) -> Optional["AIResponse"]:
        return cls._get_item(
            consistent_read=consistent_read,
            attributes_to_get=attributes_to_get,
            prompt_name=prompt_name,
            version=version,
            key=key,
            **kwargs
        )




