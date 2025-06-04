from common.dynamodb.model.MyModel import MyModel
from .Sample import *
from .Prompt import *
from .AIResponse import *


class M:
    Sample = Sample
    Prompt = Prompt
    AIResponse = AIResponse


__all__ = ['M', 'MyModel']
