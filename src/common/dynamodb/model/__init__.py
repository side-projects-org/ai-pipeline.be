from common.dynamodb.model.MyModel import MyModel
from .Sample import *
from .Prompt import *
from .AiResponse import *


class M:
    Sample = Sample
    Prompt = Prompt
    AiResponse = AiResponse


__all__ = ['M', 'MyModel']
