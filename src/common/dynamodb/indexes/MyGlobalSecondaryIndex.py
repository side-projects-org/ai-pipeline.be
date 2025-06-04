from abc import abstractmethod, ABCMeta

from pynamodb.indexes import GlobalSecondaryIndex, AllProjection


class MyGlobalSecondaryIndex(GlobalSecondaryIndex, metaclass=ABCMeta):
    class Meta:
        projection = AllProjection()
        index_name = None

    @abstractmethod
    def get_index_pk_name(self) -> str:
        """
        Abstract method to get the partition key name for the index.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_index_sk_name(self) -> str:
        """
        Abstract method to get the sort key name for the index.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def build_index_pk(self, **kwargs) -> str:
        """
        Abstract method to build the index name.
        Must be implemented by subclasses.
        """
        pass


    @abstractmethod
    def build_index_sk(self, **kwargs) -> str:
        """
        Abstract method to build the sort key for the index.
        Must be implemented by subclasses.
        """
        pass

