from datetime import datetime, timedelta
from typing import List, Optional
from ..domain.reservation import Reservation

class ReservationDAO:
    def __init__(self):
        # Stub data matching your Reservation domain model
        now = datetime.now()
        self.reservations = [
            Reservation(
                reservation_id=1,
                table_id=1,
                customer_name="John Doe",
                people_count=4,
                time=(now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
            ),
            Reservation(
                reservation_id=2,
                table_id=3,
                customer_name="Jane Smith",
                people_count=2,
                time=(now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
            )
        ]
        self.next_id = 3  # Track next available ID

    def find(self, reservation_id: int) -> Optional[Reservation]:
        """Find a reservation by its ID."""
        return next(
            (r for r in self.reservations if r.reservation_id == reservation_id), 
            None
        )

    def find_all(self) -> List[Reservation]:
        """Get all reservations."""
        return self.reservations

    def find_by_table(self, table_id: int) -> List[Reservation]:
        """Find all reservations for a specific table."""
        return [r for r in self.reservations if r.table_id == table_id]

    def find_by_customer(self, customer_name: str) -> List[Reservation]:
        """Find all reservations for a specific customer."""
        return [
            r for r in self.reservations 
            if r.customer_name.lower() == customer_name.lower()
        ]

    def save(self, reservation: Reservation) -> Reservation:
        """
        Save a reservation (create or update).
        Returns the saved reservation with updated ID if new.
        """
        if reservation.reservation_id == 0:  # New reservation
            reservation.reservation_id = self.next_id
            self.next_id += 1
            self.reservations.append(reservation)
        else:  # Update existing
            existing = self.find(reservation.reservation_id)
            if existing:
                existing.table_id = reservation.table_id
                existing.customer_name = reservation.customer_name
                existing.people_count = reservation.people_count
                existing.time = reservation.time
        return reservation

    def delete(self, reservation_id: int) -> bool:
        """
        Delete a reservation by ID.
        Returns True if deleted, False if not found.
        """
        initial_count = len(self.reservations)
        self.reservations = [
            r for r in self.reservations 
            if r.reservation_id != reservation_id
        ]
        return len(self.reservations) < initial_count

    def get_available_tables(self, time: str, people_count: int) -> List[int]:
        """
        Get list of available table IDs that can accommodate the party size
        at the requested time.
        """
        # This would need access to table data - you might want to inject TableDAO
        # For now, returns stub data
        all_tables = [1, 2, 3, 4, 5, 6]  # Example table IDs
        reserved_tables = [
            r.table_id for r in self.reservations 
            if r.time == time
        ]
        return [t for t in all_tables if t not in reserved_tables]