import uuid
from abc import ABCMeta, abstractmethod
from datetime import datetime, timezone
from typing import Dict, Any, Optional, override, Type, Sequence, Text, TypeVar

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.expressions.condition import Condition
from pynamodb.models import Model

_T = TypeVar('_T', bound='Model')

from common import APIException, ErrorCode


class ModelMetaclass(ABCMeta, type(Model)):
    pass

def default_for_new_utc_datetime() -> datetime:
    return datetime.now(timezone.utc)

def default_for_new_uuid() -> str:
    return str(uuid.uuid4())

class MyModel(Model, metaclass=ModelMetaclass):
    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)

    key = UnicodeAttribute(null=False, default_for_new=default_for_new_uuid)

    created_at = UTCDateTimeAttribute(null=True, default_for_new=default_for_new_utc_datetime)

    GSIs = []

    @classmethod
    def _get_item(
        cls: Type[_T],
        *,
        consistent_read: bool = True,
        attributes_to_get: Optional[Sequence[Text]] = None,
        **kwargs: Any
    ) -> Optional[_T]:
        """
        Generic get method. Subclasses wrap this for better IDE support.
        """
        hash_key = cls.build_pk(**kwargs)
        range_key = cls.build_sk(**kwargs)

        try:
            return cls.get(
                hash_key=hash_key,
                range_key=range_key,
                consistent_read=consistent_read,
                attributes_to_get=attributes_to_get,
            )
        except cls.DoesNotExist:
            return None
        except Exception as e:
            raise APIException(ErrorCode.DYNAMO_EXCEPTION, detail=f"Error getting item: {e}")

    def build_all_keys(self):
        if not self.pk:
            self.pk = self.build_pk(**self.to_simple_dict())

        if not self.sk:
            self.sk = self.build_sk(**self.to_simple_dict())

        for gsi in self.GSIs:
            pk_val = gsi.build_index_pk(**self.to_simple_dict())
            setattr(self, gsi.get_index_pk_name(), pk_val)

            sk_val = gsi.build_index_sk(**self.to_simple_dict())
            setattr(self, gsi.get_index_sk_name(), sk_val)

    @override
    def save(self, condition: Optional[Condition] = None, *, add_version_condition: bool = True) -> Dict[str, Any]:
        """
        Save the model instance to DynamoDB.
        Override to customize save behavior if needed.
        """
        # Custom logic can be added here if necessary
        self.build_all_keys()
        return super().save(condition=condition, add_version_condition=add_version_condition)

    @classmethod
    @abstractmethod
    def build_pk(cls, **kwargs) -> str:
        """
        Abstract method to build the partition key (pk) for the model.
        Must be implemented by subclasses.
        """
        pass

    @classmethod
    @abstractmethod
    def build_sk(cls, **kwargs) -> str:
        """
        Abstract method to build the sort key (sk) for the model.
        Must be implemented by subclasses.
        """
        pass
