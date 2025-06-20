from pynamodb.attributes import UnicodeAttribute, ListAttribute, DynamicMapAttribute, NumberAttribute

from common.dynamodb.attributes import AiMessageAttribute


class AiRequestParamsAttribute(DynamicMapAttribute):
    model = UnicodeAttribute(null=True)  # 모델 이름
    messages = ListAttribute(of=AiMessageAttribute, null=True)  # 메시지 리스트
    temperature = NumberAttribute(null=True)  # 온도
    max_completion_tokens = NumberAttribute(null=True)  # 최대 토큰 수
    max_tokens = NumberAttribute(null=True)  # 최대 토큰 수
    response_format = UnicodeAttribute(null=True)  # 응답 형식
