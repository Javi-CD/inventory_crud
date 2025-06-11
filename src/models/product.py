from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    """Product model class"""
    name: str
    price: float
    id: Optional[int] = None
    
    def __str__(self) -> str:
        return f"{self.name} (${self.price})"