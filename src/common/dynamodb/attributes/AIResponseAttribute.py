from pynamodb.attributes import DynamicMapAttribute, UnicodeAttribute, NumberAttribute, ListAttribute, MapAttribute


class AIChoiceAttribute(DynamicMapAttribute):
    index = NumberAttribute(null=True)
    message = MapAttribute(null=True)
    finish_reason = UnicodeAttribute(null=True)


class AIResponseUsageAttribute(DynamicMapAttribute):
    prompt_tokens = NumberAttribute(null=True)
    completion_tokens = NumberAttribute(null=True)
    total_tokens = NumberAttribute(null=True)


class AIResponseAttribute(DynamicMapAttribute):
    id = UnicodeAttribute(null=True)
    object = UnicodeAttribute(null=True)
    created = NumberAttribute(null=True)
    model = UnicodeAttribute(null=True)

    choices = ListAttribute(of=AIChoiceAttribute, null=True)

    usage = AIResponseUsageAttribute(null=True)
