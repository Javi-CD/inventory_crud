from typing import Dict, Any, Optional

class Product:
    """Model representing a product in the inventory."""
    
    def __init__(self, id: Optional[int] = None, name: str = "", price: float = 0.0):
        self.id = id
        self.name = name
        self.price = price
    
    @classmethod
    def from_db_tuple(cls, db_tuple):
        """Create a Product instance from a database tuple."""
        if not db_tuple:
            return None
        return cls(id=db_tuple[0], name=db_tuple[1], price=float(db_tuple[2]))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Product to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }
    
    def __str__(self) -> str:
        return f"ID {self.id} - {self.name} - ${self.price:.2f}"


class Employee:
    """Model representing an employee."""
    
    def __init__(self, id: str = "", name: str = "", role: str = ""):
        self.id = id
        self.name = name
        self.role = role
    
    def to_dict(self) -> Dict[str, str]:
        """Convert Employee to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role
        }
    
    def __str__(self) -> str:
        return f"{self.name} ({self.role})"