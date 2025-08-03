import os
import sqlite3
import sys
from typing import Any, Dict, List, Optional, Tuple


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller

    Args:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
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
            parameters (Tuple[Any, ...], optional): Values to bind to the query
                placeholders. Defaults to ().

        Returns:
            sqlite3.Cursor: Cursor object after execution.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            return result

    def get_all_products(self) -> List[Tuple[Any, ...]]:
        """Retrieve all products ordered by name descending.

        Returns:
            List[Tuple[Any, ...]]: A list of tuples representing the products.
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
        """Compute and return statistics over products.

        Returns:
            Dict[str, Any]: A dictionary containing product statistics.
        """
        stats: Dict[str, Any] = {}

        # Get total count first
        total_products = self._get_total_products_count()
        stats["total_products"] = total_products

        if total_products == 0:
            return stats

        # Get all other statistics
        stats.update(self._get_price_statistics())
        stats["categories"] = self._get_product_categories()

        return stats

    def _get_total_products_count(self) -> int:
        """Get the total number of products in the database.

        Returns:
            int: Total number of products.
        """
        query = "SELECT COUNT(*) FROM products"
        cursor = self.execute_query(query)
        return cursor.fetchone()[0]

    def _get_price_statistics(self) -> Dict[str, Any]:
        """Get price-related statistics for products.

        Returns:
            Dict[str, Any]: Dictionary containing price statistics.
        """
        price_stats = {}

        # Most expensive product
        price_stats["max_price_product"] = self._get_most_expensive_product()

        # Least expensive product
        price_stats["min_price_product"] = self._get_least_expensive_product()

        # Average and total price
        price_stats["avg_price"] = self._get_average_price()
        price_stats["total_value"] = self._get_total_value()

        return price_stats

    def _get_most_expensive_product(self) -> Tuple[Any, ...]:
        """Get the most expensive product.

        Returns:
            Tuple[Any, ...]: Tuple containing (id, name, max_price).
        """
        query = "SELECT id, name, MAX(price) FROM products"
        cursor = self.execute_query(query)
        return cursor.fetchone()

    def _get_least_expensive_product(self) -> Tuple[Any, ...]:
        """Get the least expensive product.

        Returns:
            Tuple[Any, ...]: Tuple containing (id, name, min_price).
        """
        query = "SELECT id, name, MIN(price) FROM products"
        cursor = self.execute_query(query)
        return cursor.fetchone()

    def _get_average_price(self) -> float:
        """Get the average price of all products.

        Returns:
            float: Average price of products.
        """
        query = "SELECT AVG(price) FROM products"
        cursor = self.execute_query(query)
        return cursor.fetchone()[0]

    def _get_total_value(self) -> float:
        """Get the total value of all products.

        Returns:
            float: Sum of all product prices.
        """
        query = "SELECT SUM(price) FROM products"
        cursor = self.execute_query(query)
        return cursor.fetchone()[0]

    def _get_product_categories(self) -> List[Tuple[Any, ...]]:
        """Get product categories based on the first word of product names.

        Returns:
            List[Tuple[Any, ...]]: List of tuples containing (category, count).
        """
        query = """
            SELECT DISTINCT
                SUBSTR(name, 1, INSTR(name || " ", " ") - 1) AS category,
                COUNT(*)
            FROM products
            GROUP BY category
        """
        cursor = self.execute_query(query)
        return cursor.fetchall()
