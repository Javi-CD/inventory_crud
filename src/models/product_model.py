from typing import Dict, Any, Optional


class Product:
    """Model representing a product in the inventory."""

    def __init__(
        self, id: Optional[int] = None, name: str = "", price: float = 0.0
    ) -> None:
        """Initialize a Product instance.

        Args:
            id (Optional[int], optional): The product ID. Defaults to None.
            name (str, optional): The product name. Defaults to "".
            price (float, optional): The product price. Defaults to 0.0.
        """
        self.id = id
        self.name = name
        self.price = price

    @classmethod
    def from_db_tuple(cls, db_tuple):
        """Create a Product instance from a database tuple.

        Args:
            db_tuple (tuple): A tuple representing a product record from the database.

        Returns:
            Product: An instance of the Product class.
        """

        if not db_tuple:
            return None

        return cls(id=db_tuple[0], name=db_tuple[1], price=float(db_tuple[2]))

    def to_dict(self) -> Dict[str, Any]:
        """Convert Product to dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the product.
        """
        return {"id": self.id, "name": self.name, "price": self.price}

    def __str__(self) -> str:
        """Convert Product to string representation.

        Returns:
            str: A string representation of the product.
        """
        return f"ID {self.id} - {self.name} - ${self.price:.2f}"
