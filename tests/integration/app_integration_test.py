import os
import tempfile
import unittest

from src.core.database import DatabaseManager
from src.models import Employee
from src.ui.app import InventoryApp


class TestInventoryAppIntegration(unittest.TestCase):
    """Test the integration between different components of the Inventory App."""

    def setUp(self):
        """Set up test environment."""

        # Create a temporary database for testing
        self.temp_fd, self.temp_path = tempfile.mkstemp()
        self.old_db_path = None

    def tearDown(self):
        """Clean up after tests."""

        # If we patched the database path, restore it
        if self.old_db_path is not None:
            InventoryApp.db_path = self.old_db_path

        # Close and delete temporary database
        try:
            os.close(self.temp_fd)
        except OSError:
            pass

        try:
            os.unlink(self.temp_path)
        except (OSError, PermissionError) as e:
            print(f"Could not delete {self.temp_path}: {e}")

    def test_login_flow(self):
        """Test the login functionality flow."""

        # Create app instance but don't actually show the window
        app = InventoryApp()

        # Track what frames are displayed
        self.current_frame = None

        # Override methods to track UI changes instead of showing them
        def show_inventory(self, employee):
            self.current_frame = "inventory"
            self.test_employee = employee

        # Monkey patch the method
        InventoryApp.show_inventory = show_inventory.__get__(app)

        # Simulate login
        app._on_login_success(Employee(id="E001", name="Test User", role="Admin"))

        # Check that inventory frame is displayed
        self.assertEqual(app.current_frame, "inventory")
        self.assertEqual(app.test_employee.id, "E001")
        self.assertEqual(app.test_employee.name, "Test User")
        self.assertEqual(app.test_employee.role, "Admin")

    def test_database_integration(self):
        """Test that the app correctly integrates with the database."""
        # Patch the database path
        self.old_db_path = InventoryApp.db_path
        InventoryApp.db_path = self.temp_path

        # Create direct database manager for testing
        db = DatabaseManager(self.temp_path)

        # Add some products directly to the database
        db.add_product("Test Product 1", "100.50")
        db.add_product("Test Product 2", "200.75")

        # Verify products can be retrieved
        products = db.get_all_products()
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0][1], "Test Product 2")  # Due to ORDER BY name DESC
        self.assertEqual(float(products[0][2]), 200.75)
        self.assertEqual(products[1][1], "Test Product 1")
        self.assertEqual(float(products[1][2]), 100.50)

        # Test statistics calculation
        stats = db.get_product_stats()
        self.assertEqual(stats["total_products"], 2)
        self.assertEqual(float(stats["total_value"]), 301.25)
        self.assertEqual(float(stats["avg_price"]), 150.625)
        self.assertEqual(stats["max_price_product"][1], "Test Product 2")
        self.assertEqual(float(stats["max_price_product"][2]), 200.75)

    def test_app_initialization(self):
        """Test that the app initializes correctly."""

        # Patch the database path
        self.old_db_path = InventoryApp.db_path
        InventoryApp.db_path = self.temp_path

        # Create app instance
        app = InventoryApp()

        # Check app title
        self.assertEqual(app.app.title(), "Inventory System")

        # Check initial state is login
        login_frame = None
        for widget in app.app.winfo_children():
            if "LoginFrame" in str(type(widget)):
                login_frame = widget
                break

        # We should have a login frame
        self.assertIsNotNone(login_frame)


if __name__ == "__main__":
    unittest.main()
