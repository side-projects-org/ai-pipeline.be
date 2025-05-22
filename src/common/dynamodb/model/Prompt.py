from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, MapAttribute, ListAttribute, DynamicMapAttribute, BooleanAttribute, \
    NumberAttribute, UTCDateTimeAttribute, TTLAttribute

from common.constants import BaseConfig
from common.dynamodb.attributes.CustomAttribute import CDynamicMapAttribute

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
    role = UnicodeAttribute(null=False)  # user, assistant
    content = UnicodeAttribute(null=False)  # 메시지 내용


class AIRequestParamsAttribute(DynamicMapAttribute):
    model = UnicodeAttribute(null=True)  # 모델 이름
    messages = ListAttribute(of=AIMessageAttribute, null=True)  # 메시지 리스트
    temperature = NumberAttribute(null=True)  # 온도
    max_completion_tokens = NumberAttribute(null=True)  # 최대 토큰 수
    max_tokens = NumberAttribute(null=True)  # 최대 토큰 수
    response_format = UnicodeAttribute(null=True)  # 응답 형식


class Version_PromptName_Index(GlobalSecondaryIndex):
    class Meta:
        index_name = "version-prompt_name-index"
        projection = AllProjection()

    version = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute(range_key=True)


class PromptName_Version_Index(GlobalSecondaryIndex):
    class Meta:
        index_name = "prompt_name-version-index"
        projection = AllProjection()

    prompt_name = UnicodeAttribute(hash_key=True)
    version = UnicodeAttribute(range_key=True)



class PromptName_CreatedAt_Index(GlobalSecondaryIndex):
    class Meta:
        index_name = "prompt_name-created_at-index"
        projection = AllProjection()

    prompt_name = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute(range_key=True)



class Prompt(Model):
    key = UnicodeAttribute(hash_key=True)

    prompt_name = UnicodeAttribute(null=False)  # 프롬프트의 이름
    version = UnicodeAttribute(null=False)  # 버전

    item_type = UnicodeAttribute(null=False, default="prompt")  # 아이템 타입

    params = AIRequestParamsAttribute(null=True)

    applied_version = UnicodeAttribute(null=True)  # 적용된 버전
    created_at = UTCDateTimeAttribute(null=True)  # 생성일
    updated_at = UTCDateTimeAttribute(null=True)  # 생성일

    best_ai = UnicodeAttribute(null=True)  # 가장 좋은 AI
    best_model = UnicodeAttribute(null=True)  # 가장 좋은 모델

    # gsi
    # TODO item_type 추가 해야함
    prompt_name__version__index = PromptName_Version_Index()
    prompt_name__created_at__index = PromptName_CreatedAt_Index()
    version__prompt_name__index = Version_PromptName_Index()


    class Meta:
        table_name = f"{BaseConfig.PROJECT_NAME}_{BaseConfig.STAGE_NAME}_prompt"
        region = BaseConfig.AWS_REGION

