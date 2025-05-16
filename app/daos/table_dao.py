from app.domain.table import Table
from app.daos.dao_abs import DAO
from typing import List, Optional
from db.database import get_session
from sqlalchemy.orm import Session

class TableDAO(DAO):
    """
    Data Access Object (DAO) for managing tables using SQLAlchemy.
    """

    def __init__(self, session: Optional[Session] = None):
        if session is None:
            self.session = get_session()
        else:
            self.session = session


    def find(self, id: int) -> Optional[Table]:
        """Retrieve a table by its ID."""
        return self.session.get(Table, id)

    def findAll(self) -> List[Table]:
        """Retrieve all tables."""
        return self.session.query(Table).all()

    def find_by_location(self, location: str) -> List[Table]:
        """Retrieve tables by location."""
        return self.session.query(Table).filter(Table.location == location).all()

    def save(self, table: Table) -> Table:
        """Save a new table."""
        try:
            self.session.add(table)
            self.session.commit()
            self.session.refresh(table)
            return table
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error saving table: {e}")

    def update(self, table_id: int, updated_table: Table) -> Table:
        """Update an existing table."""
        table = self.session.get(Table, table_id)
        if not table:
            raise ValueError(f"Table with ID {table_id} does not exist.")

        table.capacity = updated_table.capacity
        table.location = updated_table.location

        try:
            self.session.commit()
            self.session.refresh(table)
            return table
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating table: {e}")

    def delete(self, id: int) -> None:
        """Delete a table by ID."""
        table = self.session.get(Table, id)
        if table:
            try:
                self.session.delete(table)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise ValueError(f"Error deleting table: {e}")