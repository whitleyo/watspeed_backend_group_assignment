class MenuItemResponseDTO:
    # Attributes:
    # - id: int - menu item ID
    # - name: str - item name
    # - description: str - item description
    # - sizes: list[str] - available sizes
    # - prices: dict - mapping of size to price

    def __init__(self, id, name, description, sizes, prices):
        self.id = id
        self.name = name
        self.description = description
        self.sizes = sizes
        self.prices = prices
