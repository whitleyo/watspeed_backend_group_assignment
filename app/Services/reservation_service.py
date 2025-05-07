from typing import List, Optional, Dict, Any
from datetime import datetime
from ..domain.reservation import Reservation
from ..daos.reservation_dao import ReservationDAO
from ..daos.table_dao import TableDAO

class ReservationService:
    """
    Service layer for handling reservation business logic.
    """
    
    def __init__(self, reservation_dao: ReservationDAO, table_dao: TableDAO):
        """
        Initialize with required DAOs.
        
        Args:
            reservation_dao: Data access object for reservations
            table_dao: Data access object for tables
        """
        self.reservation_dao = reservation_dao
        self.table_dao = table_dao
    
    def create_reservation(
        self, 
        table_id: int, 
        customer_name: str, 
        people_count: int, 
        time: str
    ) -> Optional[Reservation]:
        """
        Create a new reservation after validating constraints.
        
        Args:
            table_id: ID of table to reserve
            customer_name: Name of customer making reservation
            people_count: Number of people in the party
            time: Reservation time as string
            
        Returns:
            Reservation if created successfully, None otherwise
        """
        # Validate table exists and can accommodate party size
        table = self.table_dao.find(table_id)
        if not table:
            return None
            
        if people_count > table.capacity:
            return None
            
        # Check if table is already reserved at this time
        existing = self.reservation_dao.find_by_table(table_id)
        for res in existing:
            if res.time == time:
                return None
                
        # Create and save new reservation
        new_reservation = Reservation(
            reservation_id=0,  # Will be assigned by DAO
            table_id=table_id,
            customer_name=customer_name,
            people_count=people_count,
            time=time
        )
        
        return self.reservation_dao.save(new_reservation)
    
    def get_reservation(self, reservation_id: int) -> Optional[Reservation]:
        """
        Get a reservation by ID.
        """
        return self.reservation_dao.find(reservation_id)
    
    def get_customer_reservations(self, customer_name: str) -> List[Reservation]:
        """
        Get all reservations for a customer.
        """
        return self.reservation_dao.find_by_customer(customer_name)
    
    def update_reservation(
        self,
        reservation_id: int,
        **updates: Dict[str, Any]
    ) -> Optional[Reservation]:
        """
        Update an existing reservation.
        
        Args:
            reservation_id: ID of reservation to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Reservation if successful, None otherwise
        """
        reservation = self.reservation_dao.find(reservation_id)
        if not reservation:
            return None
            
        # Validate table capacity if table is being changed
        if 'table_id' in updates:
            table = self.table_dao.find(updates['table_id'])
            if not table:
                return None
            if 'people_count' in updates:
                if updates['people_count'] > table.capacity:
                    return None
            elif reservation.people_count > table.capacity:
                return None
                
        # Apply updates
        for field, value in updates.items():
            if hasattr(reservation, field):
                setattr(reservation, field, value)
                
        return self.reservation_dao.save(reservation)
    
    def cancel_reservation(self, reservation_id: int) -> bool:
        """
        Cancel a reservation by ID.
        
        Returns:
            True if canceled successfully, False otherwise
        """
        return self.reservation_dao.delete(reservation_id)
    
    def get_available_tables(
        self, 
        time: str, 
        people_count: int
    ) -> List[Dict[str, Any]]:
        """
        Get available tables that can accommodate a party size at a given time.
        
        Returns:
            List of table dictionaries with id and capacity
        """
        all_tables = self.table_dao.findAll()
        reserved_tables = [
            r.table_id for r in self.reservation_dao.findAll() 
            if r.time == time
        ]
        
        return [
            {'id': t.id, 'capacity': t.capacity}
            for t in all_tables
            if t.id not in reserved_tables and t.capacity >= people_count
        ]