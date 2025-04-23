class OrderResponseDTO:
    # Attributes:
    # - order_id: int - order ID
    # - status: str - order status
    # - message: str - optional confirmation message

    def __init__(self, order_id, status, message):
        self.order_id = order_id
        self.status = status
        self.message = message
