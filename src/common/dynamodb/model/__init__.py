from common.dynamodb.model.MyModel import MyModel
from .Sample import *
from .Prompt import *


class M:
    Sample = Sample
    Prompt = Prompt

__all__ = ['M', 'MyModel']
