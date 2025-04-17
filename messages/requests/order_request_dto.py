class OrderRequestDTO:
    # Attributes:
    # - items: list[str] - coffee item names
    # - size: str - coffee size
    # - user_id: int - user placing the order

    def __init__(self, items, size, user_id):
        self.items = items
        self.size = size
        self.user_id = user_id


class ModifyOrderRequestDTO:
    # Attributes:
    # - order_id: int - existing order ID
    # - items: list[str] - updated items
    # - size: str - updated size

    def __init__(self, order_id, items, size):
        self.order_id = order_id
        self.items = items
        self.size = size
