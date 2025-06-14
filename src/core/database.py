import sqlite3
from typing import Any, Dict, List, Optional, Tuple
import sys
import os


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class DatabaseManager:
    """
    Manages SQLite database operations for inventory products.
    """

    def __init__(self, db_path: str) -> None:
        """Initialize DatabaseManager, creating tables if not present.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path: str = db_path
        self._create_tables()

    def _create_tables(self) -> None:
        """
        Create necessary tables if they do not exist.
        Currently creates a 'products' table with id, name, and price.
        """
        self.execute_query(
            """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        """
        )

    def execute_query(
        self, query: str, parameters: Tuple[Any, ...] = ()
    ) -> sqlite3.Cursor:
        """Execute a given SQL query with parameters, commit, and return the cursor.

        Args:
            query (str): SQL query string, possibly with placeholders.
            parameters (Tuple[Any, ...], optional): Values to bind to the query placeholders. Defaults to ().

        Returns:
            sqlite3.Cursor: Cursor object after execution.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            return result

    def get_all_products(self) -> List[Tuple[Any, ...]]:
        """
        Retrieve all products ordered by name descending.
        :return: list of tuples (id, name, price)
        """
        query = "SELECT * FROM products ORDER BY name DESC"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def add_product(self, name: str, price: str) -> None:
        """Add a new product to the database.

        Args:
            name (str): The name of the product.
            price (str): The price of the product.
        """
        query = "INSERT INTO products VALUES(NULL, ?, ?)"
        self.execute_query(query, (name, price))

    def delete_product(self, product_id: int) -> None:
        """Delete a product by ID.

        Args:
            product_id (int): The ID of the product to delete.
        """
        query = "DELETE FROM products WHERE id = ?"
        self.execute_query(query, (product_id,))

    def update_product(self, product_id: int, new_name: str, new_price: str) -> None:
        """Update an existing product's name and price.

        Args:
            product_id (int): The ID of the product to update.
            new_name (str): The new name for the product.
            new_price (str): The new price for the product.
        """
        query = "UPDATE products SET name = ?, price = ? WHERE id = ?"
        self.execute_query(query, (new_name, new_price, product_id))

    def get_product_by_id(self, product_id: int) -> Optional[Tuple[Any, ...]]:
        """Retrieve a single product by ID.

        Args:
            product_id (int): The ID of the product to retrieve.

        Returns:
            Optional[Tuple[Any, ...]]: A tuple (id, name, price) or None if not found.
        """
        query = "SELECT * FROM products WHERE id = ?"
        cursor = self.execute_query(query, (product_id,))
        return cursor.fetchone()

    def get_product_stats(self) -> Dict[str, Any]:
        """
        Compute and return statistics over products:
        - total_products: int
        - max_price_product: tuple (id, name, max_price)
        - min_price_product: tuple (id, name, min_price)
        - avg_price: float
        - total_value: float (sum of prices; adjust if quantity field is added later)
        - categories: list of tuples (category_name, count)
          Here 'category' is derived as the first word of product name.
        :return: dict with statistics
        """
        stats: Dict[str, Any] = {}

        # Total number of products
        count_query = "SELECT COUNT(*) FROM products"
        cursor = self.execute_query(count_query)
        total = cursor.fetchone()[0]
        stats["total_products"] = total

        if total == 0:
            # No further stats if empty
            return stats

        # Most expensive product (id, name, max price)
        max_query = "SELECT id, name, MAX(price) FROM products"
        cursor = self.execute_query(max_query)
        stats["max_price_product"] = cursor.fetchone()

        # Least expensive product
        min_query = "SELECT id, name, MIN(price) FROM products"
        cursor = self.execute_query(min_query)
        stats["min_price_product"] = cursor.fetchone()

        # Average price
        avg_query = "SELECT AVG(price) FROM products"
        cursor = self.execute_query(avg_query)
        stats["avg_price"] = cursor.fetchone()[0]

        # Total value (sum of prices)
        sum_query = "SELECT SUM(price) FROM products"
        cursor = self.execute_query(sum_query)
        stats["total_value"] = cursor.fetchone()[0]

        # Categories: first word of name as category, count occurrences
        categories_query = """
            SELECT DISTINCT
                SUBSTR(name, 1, INSTR(name || " ", " ") - 1) AS category,
                COUNT(*)
            FROM products
            GROUP BY category
        """
        cursor = self.execute_query(categories_query)
        stats["categories"] = cursor.fetchall()

        return stats
