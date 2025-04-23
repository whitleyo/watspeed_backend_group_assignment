class Order:
    # Attributes:
    # - id: int - unique order ID
    # - user_id: int - ID of the user who placed the order
    # - items: list[str] - list of coffee item names in the order
    # - size: str - coffee size ("small", "medium", "large")
    # - status: str - order status ("pending", "ready", "completed", etc.)
    # - timestamp: str - ISO timestamp of order creation

    def __init__(self, id, user_id, items, size, status, timestamp):
        self.id = id
        self.user_id = user_id
        self.items = items
        self.size = size
        self.status = status
        self.timestamp = timestamp
