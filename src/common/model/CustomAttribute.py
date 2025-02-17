from pynamodb.attributes import MapAttribute, DynamicMapAttribute


class CMapAttribute(MapAttribute):
    def as_dict(self):
        result = super().as_dict()
        if "attribute_values" in result and result["attribute_values"] == {}:
            del result["attribute_values"]

        return result


class CDynamicMapAttribute(DynamicMapAttribute):
    def as_dict(self):
        result = super().as_dict()
        if "attribute_values" in result and result["attribute_values"] == {}:
            del result["attribute_values"]

        return result

