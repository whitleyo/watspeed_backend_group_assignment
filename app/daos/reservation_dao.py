from typing import List, Optional
from sqlalchemy.orm import Session
from ..domain.reservation import Reservation  # Assuming a Reservation domain class
from .dao_abs import DAO

class ReservationDAO(DAO):
    """DAO for managing table reservations."""

    def __init__(self, session: Session):
        self.session = session

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

