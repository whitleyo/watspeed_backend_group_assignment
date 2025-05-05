class Table:
    """
    Domain model representing a café table that can be reserved.
    
    Attributes:
        id (int): Unique identifier for the table
        shop_id (int): ID of the shop where this table is located
        capacity (int): Maximum number of people the table can accommodate
    """
    
    def __init__(self, id: int, shop_id: int, capacity: int):
        """
        Initialize a Table instance.
        
        Args:
            id: Unique identifier for the table
            shop_id: ID of the shop where this table is located
            capacity: Maximum number of people the table can accommodate
        """
        self.id = id
        self.shop_id = shop_id
        self.capacity = capacity
    
    def to_dict(self) -> dict:
        """
        Convert the Table instance to a dictionary.
        
        Returns:
            dict: Dictionary representation of the table
        """
        return {
            'id': self.id,
            'shop_id': self.shop_id,
            'capacity': self.capacity
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Table':
        """
        Create a Table instance from a dictionary.
        
        Args:
            data: Dictionary containing table attributes
            
        Returns:
            Table: New Table instance
        """
        return cls(
            id=data['id'],
            shop_id=data['shop_id'],
            capacity=data['capacity']
        )
    
    def __eq__(self, other: object) -> bool:
        """
        Compare two Table instances for equality.
        
        Args:
            other: Another object to compare with
            
        Returns:
            bool: True if tables have same attributes, False otherwise
        """
        if not isinstance(other, Table):
            return False
        return (self.id == other.id and 
                self.shop_id == other.shop_id and 
                self.capacity == other.capacity)
    
    def __repr__(self) -> str:
        """
        Return a string representation of the Table.
        
        Returns:
            str: String representation
        """
        return f"Table(id={self.id}, shop_id={self.shop_id}, capacity={self.capacity})"