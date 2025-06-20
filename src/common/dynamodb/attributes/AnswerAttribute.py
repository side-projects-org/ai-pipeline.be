from pynamodb.attributes import DynamicMapAttribute, UnicodeAttribute, NumberAttribute, ListAttribute, MapAttribute


class ChoiceAttribute(DynamicMapAttribute):
    index = NumberAttribute(null=True)
    message = MapAttribute(null=True)
    finish_reason = UnicodeAttribute(null=True)


class AnswerUsageAttribute(DynamicMapAttribute):
    prompt_tokens = NumberAttribute(null=True)
    completion_tokens = NumberAttribute(null=True)
    total_tokens = NumberAttribute(null=True)


class AnswerAttribute(DynamicMapAttribute):
    id = UnicodeAttribute(null=True)
    object = UnicodeAttribute(null=True)
    created = NumberAttribute(null=True)
    model = UnicodeAttribute(null=True)

    choices = ListAttribute(of=ChoiceAttribute, null=True)

    usage = AnswerUsageAttribute(null=True)
