from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, MapAttribute, ListAttribute, DynamicMapAttribute, BooleanAttribute, \
    NumberAttribute, UTCDateTimeAttribute, TTLAttribute

from common.constants import BaseConfig
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

class AIMessageAttribute(MapAttribute):
    # TODO 외부로 뺄 것
    role = UnicodeAttribute(null=False)  # user, assistant
    content = UnicodeAttribute(null=False)  # 메시지 내용


class AIRequestParamsAttribute(DynamicMapAttribute):
    model = UnicodeAttribute(null=True)  # 모델 이름
    messages = ListAttribute(of=AIMessageAttribute, null=True)  # 메시지 리스트
    temperature = NumberAttribute(null=True)  # 온도
    max_completion_tokens = NumberAttribute(null=True)  # 최대 토큰 수
    max_tokens = NumberAttribute(null=True)  # 최대 토큰 수
    response_format = UnicodeAttribute(null=True)  # 응답 형식


class Version_PromptName_Index(MyGlobalSecondaryIndex):
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
        # TODO created_at 이 인스턴스 생성 시점인지, 디비에 저장된 시점인지에 따라 문제발생 가능성 있음
        # UTCDateTimeAttribute 를 사용하고 있으므로 저장했을 떄 어떻게 생겼을지 모름
        return f"{item_type}#created_at@{created_at}"

    class Meta:
        index_name = "prompt_name-item_type__created_at-index"
        projection = AllProjection()

    prompt_name = UnicodeAttribute(hash_key=True)
    item_type__created_at = UnicodeAttribute(range_key=True)



class Prompt(MyModel):
    def build_pk(self) -> str:
        return f"{self.prompt_name}"

    def build_sk(self) -> str:
        return f"{self.item_type}#version@{self.version}"

    pk = UnicodeAttribute(hash_key=True)  # 파티션 키
    sk = UnicodeAttribute(range_key=True)  # 정렬 키

    item_type = UnicodeAttribute(null=False, default="PROMPT")  # 아이템 타입

    prompt_name = UnicodeAttribute(null=False)  # 프롬프트의 이름
    version = UnicodeAttribute(null=False)  # 버전

    params = AIRequestParamsAttribute(null=True)

    applied_version = UnicodeAttribute(null=True)  # 적용된 버전
    created_at = UTCDateTimeAttribute(null=True)  # 생성일
    updated_at = UTCDateTimeAttribute(null=True)  # 생성일

    best_ai = UnicodeAttribute(null=True)  # 가장 좋은 AI
    best_model = UnicodeAttribute(null=True)  # 가장 좋은 모델

    # gsi
    pk_prompt_name_sk_item_type__created_at_index = PromptName_ItemTypeCreatedAt_Index()
    version__prompt_name__index = Version_PromptName_Index()

    GSIs = [
        pk_prompt_name_sk_item_type__created_at_index,
        version__prompt_name__index
    ]

    class Meta:
        table_name = f"{BaseConfig.PROJECT_NAME}_{BaseConfig.STAGE_NAME}_prompt"
        region = BaseConfig.AWS_REGION

