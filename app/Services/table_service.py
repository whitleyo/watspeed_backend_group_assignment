from typing import List, Optional
from ..domain.table import Table
from ..daos.table_dao import TableDAO

class TableService:
    """
    Service layer for handling table-related business logic.
    """
    
    def __init__(self, table_dao: TableDAO):
        """
        Initialize with table DAO.
        """
        self.table_dao = table_dao
    
    def get_table(self, table_id: int) -> Optional[Table]:
        """
        Get a table by ID.
        """
        return self.table_dao.find(table_id)
    
    def get_all_tables(self) -> List[Table]:
        """
        Get all tables.
        """
        return self.table_dao.findAll()
    
    def get_tables_by_location(self, location: str) -> List[Table]:
        """
        Get all tables in a specific shop.
        """
        return self.table_dao.find_by_location(location)
    
    def get_table_capacity(self, table_id: int) -> Optional[int]:
        """
        Get capacity of a specific table.
        """
        table = self.table_dao.find(table_id)
        return table.capacity if table else None