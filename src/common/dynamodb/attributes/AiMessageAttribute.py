from pynamodb.attributes import UnicodeAttribute, MapAttribute


class AiMessageAttribute(MapAttribute):
    role = UnicodeAttribute(null=False)  # user, assistant, system
    content = UnicodeAttribute(null=False)  # 메시지 내용


