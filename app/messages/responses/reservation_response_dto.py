class ReservationResponseDTO:
    # Attributes:
    # - table_id: int - table id
    # - customer_name: str - name of the customer making the reservation
    # - people_count: int - number of people for the reservation
    # - time: str - time of the reservation (could be a datetime object)

    def __init__(self, table_id, customer_name, people_count, time):
        self.table_id = table_id
        self.customer_name = customer_name
        self.people_count = people_count
        self.time = time