from typing import List, Optional
from ..domain.reservation import Reservation  # Assuming a Reservation domain class
from .dao_abs import DAO
from db.database import get_session

class ReservationDAO(DAO):
    """DAO for managing table reservations."""

    def __init__(self):
        self.session = get_session()

    def find(self, reservation_id: int) -> Optional[Reservation]:
        """Retrieve a reservation by ID."""
        return self.session.get(Reservation, reservation_id)

    def findAll(self) -> List[Reservation]:
        """Retrieve all reservations."""
        return self.session.query(Reservation).all()

    def save(self, reservation: Reservation) -> Reservation:
        """Save a new reservation."""
        try:
            self.session.add(reservation)
            self.session.commit()
            self.session.refresh(reservation)
            return reservation
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error saving reservation: {e}")

    def update(self, reservation_id: int, updated_reservation: Reservation) -> Reservation:
        """Update an existing reservation."""
        reservation = self.session.get(Reservation, reservation_id)
        if not reservation:
            raise ValueError(f"Reservation with ID {reservation_id} does not exist.")

        reservation.table_id = updated_reservation.table_id
        reservation.customer_name = updated_reservation.customer_name
        reservation.people_count = updated_reservation.people_count
        reservation.time = updated_reservation.time

        try:
            self.session.commit()
            self.session.refresh(reservation)
            return reservation
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating reservation: {e}")

    def delete(self, reservation_id: int) -> None:
        """Delete a reservation by ID."""
        reservation = self.session.get(Reservation, reservation_id)
        if reservation:
            try:
                self.session.delete(reservation)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise ValueError(f"Error deleting reservation: {e}")

    def find_by_table(self, table_id: int) -> List[Reservation]:
        """
        Retrieve all reservations for a specific table.
        """
        return self.session.query(Reservation).filter_by(table_id=table_id).all()