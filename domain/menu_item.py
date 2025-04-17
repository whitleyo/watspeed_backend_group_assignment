class MenuItem:
    # Attributes:
    # - id: int - unique menu item ID
    # - name: str - name of the coffee item
    # - description: str - brief description of the item
    # - sizes: list[str] - available sizes (e.g., ["small", "medium", "large"])
    # - prices: dict - price per size, e.g., { "small": 3.0, "medium": 3.5, "large": 4.0 }

    def __init__(self, id, name, description, sizes, prices):
        self.id = id
        self.name = name
        self.description = description
        self.sizes = sizes
        self.prices = prices
