# pynamodb 의 model 을 dict 로 변환하는 메서드
import datetime

from pynamodb.attributes import MapAttribute, DynamicMapAttribute, TTLAttribute
from pynamodb.models import Model


def _model_to_dict(model):
    for attr_name in model.get_attributes().keys():
        attr = getattr(model, attr_name)
        if isinstance(attr, MapAttribute) or isinstance(attr, DynamicMapAttribute):
            attr = dict(model_to_dict(attr))
        elif isinstance(attr, list):
            attr = [dict(model_to_dict(item)) if isinstance(item, MapAttribute) or isinstance(item, DynamicMapAttribute) else item for item in attr]
        yield attr_name, attr


def model_to_dict(model: Model):
    return dict(_model_to_dict(model))