import unittest
import customtkinter as ctk
import tempfile
import os
from src.ui.components.stats_panel import StatisticsPanel
from src.ui.components.components import MessageLabel
from src.core.database import DatabaseManager
from src.ui.styles import AppStyles


class TestStatisticsPanel(unittest.TestCase):
    """Test the statistics panel functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests."""
        cls.root = ctk.CTk()
        AppStyles.setup()

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        cls.root.destroy()

    def setUp(self):
        """Set up before each test."""

        # Create a temporary database for testing
        self.temp_fd, self.temp_path = tempfile.mkstemp()
        self.db_manager = DatabaseManager(self.temp_path)

        # Create parent frame
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack()

        # Create message label
        self.message_label = MessageLabel(self.frame)
        self.message_label.pack()

        # Create stats panel
        self.stats_panel = StatisticsPanel(
            self.frame, self.db_manager, self.message_label
        )

    def tearDown(self):
        """Clean up after each test."""

        self.frame.destroy()

        # Close database connection and remove temporary file
        if hasattr(self.db_manager, "conn") and self.db_manager.conn:
            self.db_manager.conn.close()
            self.db_manager.conn = None

        # Try to close the file descriptor and delete the file
        try:
            os.close(self.temp_fd)
        except OSError:
            pass

        try:
            os.unlink(self.temp_path)
        except (OSError, PermissionError) as e:
            print(f"Could not delete {self.temp_path}: {e}")

    def test_empty_statistics(self):
        """Test statistics display with no products in database."""
        self.stats_panel.update_stats()

        # Check labels
        self.assertEqual(self.stats_panel.total_products_label.cget("text"), "0")
        self.assertEqual(self.stats_panel.total_value_label.cget("text"), "No products")
        self.assertEqual(self.stats_panel.avg_price_label.cget("text"), "N/A")
        self.assertEqual(self.stats_panel.max_price_label.cget("text"), "N/A")
        self.assertEqual(self.stats_panel.min_price_label.cget("text"), "N/A")

        # Check message
        self.assertEqual(
            self.message_label.cget("text"), "No products to show statistics."
        )

    def test_statistics_with_products(self):
        """Test statistics display with products in database."""
        # Add test products
        self.db_manager.add_product("Laptop Dell", "1000.00")
        self.db_manager.add_product("Laptop HP", "800.00")
        self.db_manager.add_product("Mouse Logitech", "30.00")

        # Update statistics
        self.stats_panel.update_stats()

        # Check labels
        self.assertEqual(self.stats_panel.total_products_label.cget("text"), "3")
        self.assertEqual(self.stats_panel.total_value_label.cget("text"), "$1,830.00")
        self.assertEqual(self.stats_panel.avg_price_label.cget("text"), "$610.00")

        # Check max price product (Laptop Dell)
        self.assertTrue("Laptop Dell" in self.stats_panel.max_price_label.cget("text"))
        self.assertTrue("$1,000.00" in self.stats_panel.max_price_label.cget("text"))

        # Check min price product (Mouse Logitech)
        self.assertTrue(
            "Mouse Logitech" in self.stats_panel.min_price_label.cget("text")
        )
        self.assertTrue("$30.00" in self.stats_panel.min_price_label.cget("text"))

        # Check message
        self.assertEqual(self.message_label.cget("text"), "Statistics updated.")

    def test_category_counting(self):
        """Test that categories are correctly counted and displayed."""

        # Add test products with different categories
        self.db_manager.add_product("Laptop Dell", "1000.00")
        self.db_manager.add_product("Laptop HP", "800.00")
        self.db_manager.add_product("Mouse Logitech", "30.00")
        self.db_manager.add_product("Mouse Microsoft", "25.00")
        self.db_manager.add_product("Keyboard Logitech", "50.00")

        # Update statistics
        self.stats_panel.update_stats()

        # Get categories from database (should have Laptop: 2, Mouse: 2, Keyboard: 1)
        stats = self.db_manager.get_product_stats()
        categories = {category: count for category, count in stats["categories"]}

        self.assertEqual(categories["Laptop"], 2)
        self.assertEqual(categories["Mouse"], 2)
        self.assertEqual(categories["Keyboard"], 1)


if __name__ == "__main__":
    unittest.main()
