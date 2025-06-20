from .MyAttribute import CDynamicMapAttribute

from .AIMessageAttribute import AIMessageAttribute
from .AIRequestParamsAttribute import AIRequestParamsAttribute
from .AnswerAttribute import AnswerAttribute, ChoiceAttribute, AnswerUsageAttribute

class Attr:
    AIRequestParamsAttribute = AIRequestParamsAttribute
    AIMessageAttribute = AIMessageAttribute
    AnswerAttribute = AnswerAttribute
    ChoiceAttribute = ChoiceAttribute
    AnswerUsageAttribute = AnswerUsageAttribute

__all__ = ['CDynamicMapAttribute', 'Attr',
           'AIMessageAttribute', 'AIRequestParamsAttribute',
           'AnswerAttribute', 'ChoiceAttribute', 'AnswerUsageAttribute']
