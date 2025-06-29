import os
import sqlite3
import tempfile
import unittest

from src.core.database import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Test database operations for the inventory system."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_fd, self.temp_path = tempfile.mkstemp()
        self.db_manager = DatabaseManager(self.temp_path)

    def tearDown(self):
        """Remove temporary database after tests."""
        # Explicitly close the connection to the database
        if hasattr(self.db_manager, "conn") and self.db_manager.conn:
            self.db_manager.conn.close()
            self.db_manager.conn = None

        # On Windows, it may be necessary to wait a bit before deleting
        import time

        time.sleep(0.1)

        # Try to close the file descriptor and delete the file
        try:
            os.close(self.temp_fd)
        except OSError:
            pass  # It may already be closed

        try:
            os.unlink(self.temp_path)
        except (OSError, PermissionError) as e:
            print(f"Could not delete {self.temp_path}: {e}")

    def test_create_tables(self):
        """Test that tables are created correctly."""

        # Check if the products table exists
        conn = sqlite3.connect(self.temp_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='products'"
        )
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "products")

    def test_add_product(self):
        """Test adding a product to the database."""

        # Add a test product
        self.db_manager.add_product("Test Product", "99.99")

        # Verify product was added
        products = self.db_manager.get_all_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][1], "Test Product")
        self.assertEqual(float(products[0][2]), 99.99)

    def test_update_product(self):
        """Test updating a product in the database."""
        # Add a test product
        self.db_manager.add_product("Original Product", "50.00")
        products = self.db_manager.get_all_products()
        product_id = products[0][0]

        # Update the product
        self.db_manager.update_product(product_id, "Updated Product", "75.50")

        # Verify update worked
        updated_product = self.db_manager.get_product_by_id(product_id)
        self.assertEqual(updated_product[1], "Updated Product")
        self.assertEqual(float(updated_product[2]), 75.50)

    def test_delete_product(self):
        """Test deleting a product from the database."""

        # Add a test product
        self.db_manager.add_product("Delete Me", "10.00")
        products = self.db_manager.get_all_products()
        product_id = products[0][0]

        # Delete the product
        self.db_manager.delete_product(product_id)

        # Verify deletion
        products_after = self.db_manager.get_all_products()
        self.assertEqual(len(products_after), 0)

    def test_get_product_by_id(self):
        """Test retrieving a product by its ID."""

        # Add a test product
        self.db_manager.add_product("Find Me", "25.75")
        products = self.db_manager.get_all_products()
        product_id = products[0][0]

        # Get product by ID
        found_product = self.db_manager.get_product_by_id(product_id)

        # Verify correct product retrieved
        self.assertIsNotNone(found_product)
        self.assertEqual(found_product[1], "Find Me")

    def test_get_product_stats_empty(self):
        """Test stats on empty database."""
        stats = self.db_manager.get_product_stats()

        self.assertEqual(stats["total_products"], 0)

    def test_get_product_stats(self):
        """Test product statistics."""

        # Add test products
        self.db_manager.add_product("Laptop XPS", "1200.00")
        self.db_manager.add_product("Laptop Thinkpad", "900.00")
        self.db_manager.add_product("Mouse Logitech", "25.00")

        stats = self.db_manager.get_product_stats()

        # Verify stats
        self.assertEqual(stats["total_products"], 3)
        self.assertEqual(float(stats["avg_price"]), (1200.00 + 900.00 + 25.00) / 3)
        self.assertEqual(float(stats["total_value"]), 1200.00 + 900.00 + 25.00)

        # Verify max and min products
        self.assertEqual(stats["max_price_product"][1], "Laptop XPS")
        self.assertEqual(float(stats["max_price_product"][2]), 1200.00)

        self.assertEqual(stats["min_price_product"][1], "Mouse Logitech")
        self.assertEqual(float(stats["min_price_product"][2]), 25.00)

        # Verify categories
        categories = {category: count for category, count in stats["categories"]}
        self.assertEqual(categories["Laptop"], 2)
        self.assertEqual(categories["Mouse"], 1)


if __name__ == "__main__":
    unittest.main()
