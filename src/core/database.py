import sqlite3
from typing import List, Tuple, Any, Optional

class DatabaseManager:
    """Database manager for the inventory application"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        
    def execute_query(self, query: str, parameters: tuple = ()) -> sqlite3.Cursor:
        """Execute a database query and return the cursor.
        
        Args:
            query: The SQL query to execute
            parameters: The parameters for the query
            
        Returns:
            sqlite3.Cursor: The cursor with the query results
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            return result
            
    def get_all_products(self) -> List[Tuple[Any, ...]]:
        """Get all products from the database.
        
        Returns:
            List[Tuple]: List of product tuples
        """
        query = 'SELECT * FROM products ORDER BY name DESC'
        cursor = self.execute_query(query)
        return cursor.fetchall()
        
    def add_product(self, name: str, price: str) -> None:
        """Add a new product to the database.
        
        Args:
            name: Product name
            price: Product price
        """
        query = 'INSERT INTO products VALUES(NULL, ?, ?)'
        self.execute_query(query, (name, price))
        
    def delete_product(self, name: str) -> None:
        """Delete a product from the database.
        
        Args:
            name: Name of the product to delete
        """
        query = 'DELETE FROM products WHERE name = ?'
        self.execute_query(query, (name,))
        
    def update_product(self, new_name: str, new_price: str, old_name: str, old_price: str) -> None:
        """Update product information.
        
        Args:
            new_name: New product name
            new_price: New product price
            old_name: Original product name
            old_price: Original product price
        """
        query = 'UPDATE products SET name = ?, price = ? WHERE name = ? AND price = ?'
        self.execute_query(query, (new_name, new_price, old_name, old_price))