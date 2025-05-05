from typing import List, Optional
from ..domain.table import Table

class TableDAO:
    def __init__(self):
        # Stub data - will be replaced with DB in Module 7
        self.tables = [
            Table(id=1, shop_id=1, capacity=4),
            Table(id=2, shop_id=1, capacity=4),
            Table(id=3, shop_id=1, capacity=4),
            Table(id=4, shop_id=1, capacity=6),
            Table(id=5, shop_id=1, capacity=6),
            Table(id=6, shop_id=1, capacity=6),
            # Second location tables
            Table(id=7, shop_id=2, capacity=4),
            Table(id=8, shop_id=2, capacity=4),
            Table(id=9, shop_id=2, capacity=4),
            Table(id=10, shop_id=2, capacity=4),
        ]

    def find(self, id: int) -> Optional[Table]:
        return next((table for table in self.tables if table.id == id), None)

    def find_all(self) -> List[Table]:
        return self.tables

    def find_by_shop(self, shop_id: int) -> List[Table]:
        return [table for table in self.tables if table.shop_id == shop_id]

    def save(self, table: Table) -> Table:
        if table.id == 0:  # New table
            new_id = max(t.id for t in self.tables) + 1
            table.id = new_id
            self.tables.append(table)
        else:  # Update existing
            existing = self.find(table.id)
            if existing:
                existing.shop_id = table.shop_id
                existing.capacity = table.capacity
        return table

    def delete(self, id: int) -> None:
        self.tables = [table for table in self.tables if table.id != id]