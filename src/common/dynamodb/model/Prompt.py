from typing import Type, Optional, Sequence, Text, Any

from pynamodb.indexes import AllProjection
from pynamodb.attributes import UnicodeAttribute, MapAttribute, ListAttribute, DynamicMapAttribute, BooleanAttribute, \
    NumberAttribute, UTCDateTimeAttribute

from common.constants import BaseConfig, ModelType
from common.dynamodb.attributes import Attr
from common.dynamodb.indexes import MyGlobalSecondaryIndex
from common.dynamodb.model import MyModel

prompt_dict_sample = {
    "key": "sample_key",
    "prompt_name": "sample_prompt_name", # 프롬프트의 이름
    "params": {
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
    "best_ai": "bedrock",
    "best_model": "claude-3.5-sonnet",
}


class Version_ItemTypePromptName_Index(MyGlobalSecondaryIndex):
    def get_index_pk_name(self) -> str:
        return "version"

    def get_index_sk_name(self) -> str:
        return "item_type__prompt_name"

    def build_index_pk(self, version=None, **kwargs) -> str:
        return f"{version}"

    def build_index_sk(self, item_type, prompt_name=None, **kwargs) -> str:
        return f"{item_type}#{prompt_name}"

    class Meta:
        index_name = "version-item_type__prompt_name-index"
        projection = AllProjection()

    version = UnicodeAttribute(hash_key=True)
    item_type__prompt_name = UnicodeAttribute(range_key=True)


class PromptName_ItemTypeCreatedAt_Index(MyGlobalSecondaryIndex):
    def get_index_pk_name(self) -> str:
        return "prompt_name"

    def get_index_sk_name(self) -> str:
        return "item_type__created_at"

    def build_index_pk(self, prompt_name=None, **kwargs) -> str:
        return f"{prompt_name}"

    def build_index_sk(self, item_type, created_at=None, **kwargs) -> str:
        return f"{item_type}#created_at@{created_at}"

    class Meta:
        index_name = "prompt_name-item_type__created_at-index"
        projection = AllProjection()

    prompt_name = UnicodeAttribute(hash_key=True)
    item_type__created_at = UnicodeAttribute(range_key=True)




class Prompt(MyModel):
    item_type = UnicodeAttribute(null=False, default=ModelType.Prompt.value)  # 아이템 타입

    prompt_name = UnicodeAttribute(null=False)  # 프롬프트의 이름
    version = UnicodeAttribute(null=False)  # 버전

    params = Attr.AIRequestParamsAttribute(null=True)

    applied_version = UnicodeAttribute(null=True)  # 적용된 버전

    updated_at = UTCDateTimeAttribute(null=True)  # 생성일

    best_ai = UnicodeAttribute(null=True)  # 가장 좋은 AI
    best_model = UnicodeAttribute(null=True)  # 가장 좋은 모델

    # gsi keys
    item_type__created_at = UnicodeAttribute(null=False)  # 아이템 타입과 생성일을 합친 키
    item_type__prompt_name = UnicodeAttribute(null=False)  # 아이템 타입과 프롬프트 이름을 합친 키

    # gsi
    pk_prompt_name_sk_item_type__created_at_index = PromptName_ItemTypeCreatedAt_Index()
    pk_version_sk_item_type__prompt_name__index = Version_ItemTypePromptName_Index()

    GSIs = [
        pk_prompt_name_sk_item_type__created_at_index,
        pk_version_sk_item_type__prompt_name__index
    ]

    class Meta:
        table_name = f"{BaseConfig.PROJECT_NAME}_{BaseConfig.STAGE_NAME}_prompt_v2"
        region = BaseConfig.AWS_REGION

    @classmethod
    def build_pk(cls, prompt_name: str, **_) -> str:
        return f"{prompt_name}"

    @classmethod
    def build_sk(cls, item_type: str, version: str, **_) -> str:
        return f"{item_type}#version@{version}"


    @classmethod
    def get_item(
            cls, prompt_name: str, version: str,
            consistent_read: bool = True,
            attributes_to_get: Optional[Sequence[Text]] = None,
            **kwargs: Any
    ) -> Optional["Prompt"]:

        return cls._get_item(consistent_read=consistent_read, attributes_to_get=attributes_to_get,
                        prompt_name=prompt_name, version=version, **kwargs)
