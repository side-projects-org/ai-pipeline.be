from .MyAttribute import CDynamicMapAttribute

from .AiMessageAttribute import AiMessageAttribute
from .AiRequestParamsAttribute import AiRequestParamsAttribute
from .AnswerAttribute import AnswerAttribute, ChoiceAttribute, AnswerUsageAttribute

class Attr:
    AiRequestParamsAttribute = AiRequestParamsAttribute
    AiMessageAttribute = AiMessageAttribute
    AnswerAttribute = AnswerAttribute
    ChoiceAttribute = ChoiceAttribute
    AnswerUsageAttribute = AnswerUsageAttribute

__all__ = ['CDynamicMapAttribute', 'Attr',
           'AiMessageAttribute', 'AiRequestParamsAttribute',
           'AnswerAttribute', 'ChoiceAttribute', 'AnswerUsageAttribute']
