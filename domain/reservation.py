
class Table:
    def __init__(self, table_id: int, seats: int):
        """
        Initialize a table with a unique ID and number of seats.
        Args:
            table_id (int): Unique identifier for the table.
            seats (int): Number of seats at the table.
        Attributes:
            table_id (int): Unique identifier for the table.
            seats (int): Number of seats at the table.
            is_reserved (bool): Reservation status of the table.
        """
        self.table_id = table_id
        self.seats = seats
        self.is_reserved = False  # Simple flag for reservation status

class Reservation:
    def __init__(self, reservation_id: int, table_id: int, customer_name: str, people_count: int, time: str):
        """
        Initialize a reservation with a unique ID, table ID, customer name, number of people, and time.
        Args:
            reservation_id (int): Unique identifier for the reservation.
            table_id (int): Unique identifier for the table being reserved.
            customer_name (str): Name of the customer making the reservation.
            people_count (int): Number of people for the reservation.
            time (str): Time of the reservation (could be a datetime object).
        """
        self.reservation_id = reservation_id
        self.table_id = table_id
        self.customer_name = customer_name
        self.people_count = people_count
        self.time = time  # Could be datetime object