import sqlite3
from typing import List, Tuple, Any, Optional

class DatabaseManager:
    """Database manager for the inventory application"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        self.execute_query('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        ''')
    
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
        
    def delete_product(self, product_id: int) -> None:
        """Delete a product from the database.
        
        Args:
            product_id: ID of the product to delete
        """
        query = 'DELETE FROM products WHERE id = ?'
        self.execute_query(query, (product_id,))
        
    def update_product(self, product_id: int, new_name: str, new_price: str) -> None:
        """Update product information.
        
        Args:
            product_id: ID of the product to update
            new_name: New product name
            new_price: New product price
        """
        query = 'UPDATE products SET name = ?, price = ? WHERE id = ?'
        self.execute_query(query, (new_name, new_price, product_id))
        
    def get_product_by_id(self, product_id: int) -> Optional[Tuple]:
        """Get a product by its ID.
        
        Args:
            product_id: ID of the product to retrieve
            
        Returns:
            Optional[Tuple]: Product tuple or None if not found
        """
        query = 'SELECT * FROM products WHERE id = ?'
        cursor = self.execute_query(query, (product_id,))
        result = cursor.fetchone()
        return result