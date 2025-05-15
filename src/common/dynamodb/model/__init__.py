from .Sample import (Sample, SampleGlobalIndex, SampleExtends, CustomMapAttribute,
                     CustomDynamicMapAttribute, CustomMyDynamicMapAttribute)
from .Prompt import *

class M:
    Sample = Sample
    Prompt = Prompt

__all__ = ['Sample', 'SampleGlobalIndex', 'SampleExtends', 'CustomMapAttribute',
           'CustomDynamicMapAttribute', 'CustomMyDynamicMapAttribute']
