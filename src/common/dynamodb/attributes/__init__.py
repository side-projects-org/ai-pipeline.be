from .MyAttribute import CDynamicMapAttribute

from .AIMessageAttribute import AIMessageAttribute
from .AIRequestParamsAttribute import AIRequestParamsAttribute
from .AIResponseAttribute import AIResponseAttribute, AIChoiceAttribute, AIResponseUsageAttribute

class Attr:
    AIRequestParamsAttribute = AIRequestParamsAttribute
    AIMessageAttribute = AIMessageAttribute
    AIResponseAttribute = AIResponseAttribute
    AIChoiceAttribute = AIChoiceAttribute
    AIResponseUsageAttribute = AIResponseUsageAttribute

__all__ = ['CDynamicMapAttribute', 'Attr',
           'AIMessageAttribute', 'AIRequestParamsAttribute',
           'AIResponseAttribute', 'AIChoiceAttribute', 'AIResponseUsageAttribute']
