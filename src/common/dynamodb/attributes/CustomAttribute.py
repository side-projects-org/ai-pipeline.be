from typing import Dict, Any

from pynamodb.attributes import MapAttribute, DynamicMapAttribute


class CDynamicMapAttribute(DynamicMapAttribute):
    """
    This class extends DynamicMapAttribute to delete the `attribute_values` key
    So, not recommended.
    But I will not delete this class because of reference in other code.
    """
    def as_dict(self):
        result = super().as_dict()
        if "attribute_values" in result and result["attribute_values"] == {}:
            del result["attribute_values"]

        return result

    def to_simple_dict(self, *, force: bool = False) -> Dict[str, Any]:
        """
        Convert the attribute to a simple dictionary representation.
        If force is True, it will include all attributes regardless of their type.
        """
        result = super().to_simple_dict(force=force)
        if "attribute_values" in result and result["attribute_values"] == {}:
            del result["attribute_values"]

        return result

