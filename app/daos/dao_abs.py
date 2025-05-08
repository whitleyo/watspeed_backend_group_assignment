from abc import ABC, abstractmethod

class DAO(ABC):
    """
    Abstract base class for Data Access Objects (DAOs).
    This class defines the interface for all DAOs in the application.
    """

    
    @abstractmethod
    def find(self, item_id):
        """
        Read an item from the data store by its ID.
        :param item_id: The ID of the item to be read.
        :return: The item with the specified ID.
        """
        pass


    @abstractmethod
    def findAll(self):
        """
        Create a new item in the data store.
        :param item: The item to be created.
        """
        pass


    @abstractmethod
    def save(self, item):
        """
        Create a new item  in the data store.
        :param item: The item to be updated.
        """
        pass

    @abstractmethod
    def update(self, item):
        """
        Update an existing item in the data store.
        :param item: The item to be updated.
        """
        pass

    @abstractmethod
    def delete(self, item_id):
        """
        Delete an item from the data store by its ID.
        :param item_id: The ID of the item to be deleted.
        """
        pass
