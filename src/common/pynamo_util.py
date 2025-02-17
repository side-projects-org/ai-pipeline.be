# pynamodb 의 model 을 dict 로 변환하는 메서드
import datetime

from pynamodb.attributes import MapAttribute, DynamicMapAttribute


def model_to_dict(model):
    for attr_name in model.get_attributes().keys():
        attr = getattr(model, attr_name)
        if isinstance(attr, MapAttribute) or isinstance(attr, DynamicMapAttribute):
            attr = attr.as_dict()
        elif isinstance(attr, list):
            attr = [dict(model_to_dict(item)) if isinstance(item, MapAttribute) or isinstance(item, DynamicMapAttribute) else item for item in attr]
        elif isinstance(attr, datetime.datetime):
            attr = datetime.datetime.strftime(attr, "%Y-%m-%dT%H:%M:%S")
        yield attr_name, attr
