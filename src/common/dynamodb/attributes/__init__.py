from .MyAttribute import CDynamicMapAttribute

from .AIMessageAttribute import AIMessageAttribute
from .AIRequestParamsAttribute import AIRequestParamsAttribute


class Attr:
    AIRequestParamsAttribute = AIRequestParamsAttribute
    AIMessageAttribute = AIMessageAttribute


__all__ = ['CDynamicMapAttribute', 'Attr', 'AIMessageAttribute', 'AIRequestParamsAttribute']
