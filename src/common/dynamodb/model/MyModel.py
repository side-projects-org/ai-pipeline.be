import uuid
from abc import ABCMeta, abstractmethod
from typing import Dict, Any, Optional, override

from pynamodb.attributes import UnicodeAttribute
from pynamodb.expressions.condition import Condition
from pynamodb.models import Model

class ModelMetaclass(ABCMeta, type(Model)):
    pass

class MyModel(Model, metaclass=ModelMetaclass):
    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)

    key = UnicodeAttribute(null=False)

    GSIs = []

    def build_all_keys(self):
        if not self.pk:
            self.pk = self.build_pk()

        if not self.sk:
            self.sk = self.build_sk()

        # UUID
        self.key = uuid.uuid4().__str__()

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

    @abstractmethod
    def build_pk(self) -> str:
        """
        Abstract method to build the partition key (pk) for the model.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def build_sk(self) -> str:
        """
        Abstract method to build the sort key (sk) for the model.
        Must be implemented by subclasses.
        """
        pass
