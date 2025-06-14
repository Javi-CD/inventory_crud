import unittest
import customtkinter as ctk
import tempfile
import os
from src.ui.components.product.product_form import ProductManagementTab
from src.ui.components.components import MessageLabel
from src.core.database import DatabaseManager
from src.ui.styles import AppStyles


class TestProductManagementTab(unittest.TestCase):
    """Test the product management form functionality."""

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

        # Track if refresh callback was called
        self.refresh_called = False

        def refresh_callback():
            self.refresh_called = True

        # Create product management tab
        self.product_tab = ProductManagementTab(
            self.frame, self.db_manager, self.message_label, refresh_callback
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

    def test_create_product_success(self):
        """Test successful product creation."""

        # Set form values
        self.product_tab.name_entry.delete(0, "end")
        self.product_tab.name_entry.insert(0, "Test Product")

        self.product_tab.price_entry.delete(0, "end")
        self.product_tab.price_entry.insert(0, "99.99")

        # Create product
        self.product_tab.create_product()

        # Check message
        self.assertEqual(
            self.message_label.cget("text"),
            "Product 'Test Product' added successfully.",
        )
        self.assertEqual(self.message_label.cget("text_color"), "#4BB543")

        # Check if refresh callback was called
        self.assertTrue(self.refresh_called)

        # Check if product was added to database
        products = self.db_manager.get_all_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][1], "Test Product")
        self.assertEqual(float(products[0][2]), 99.99)

        # Check if form was cleared
        self.assertEqual(self.product_tab.name_entry.get(), "")
        self.assertEqual(self.product_tab.price_entry.get(), "")

    def test_create_product_missing_fields(self):
        """Test product creation with missing fields."""

        # Clear form
        self.product_tab.name_entry.delete(0, "end")
        self.product_tab.price_entry.delete(0, "end")

        # Attempt to create product
        self.product_tab.create_product()

        # Check error message
        self.assertEqual(self.message_label.cget("text"), "Please complete all fields.")
        self.assertEqual(self.message_label.cget("text_color"), "#FF3333")

        # Check that refresh was not called and no product was added
        self.assertFalse(self.refresh_called)
        products = self.db_manager.get_all_products()
        self.assertEqual(len(products), 0)

    def test_create_product_invalid_price(self):
        """Test product creation with invalid price."""

        # Set form values with invalid price
        self.product_tab.name_entry.delete(0, "end")
        self.product_tab.name_entry.insert(0, "Test Product")

        self.product_tab.price_entry.delete(0, "end")
        self.product_tab.price_entry.insert(0, "not-a-number")

        # Attempt to create product
        self.product_tab.create_product()

        # Check error message
        self.assertEqual(self.message_label.cget("text"), "Price must be numeric.")
        self.assertEqual(self.message_label.cget("text_color"), "#FF3333")

        # Check that refresh was not called and no product was added
        self.assertFalse(self.refresh_called)
        products = self.db_manager.get_all_products()
        self.assertEqual(len(products), 0)

    def test_update_product_success(self):
        """Test successful product update."""

        # Add a product to update
        self.db_manager.add_product("Original Product", "50.00")
        products = self.db_manager.get_all_products()
        product_id = products[0][0]

        # Set form values for update
        self.product_tab.id_entry.delete(0, "end")
        self.product_tab.id_entry.insert(0, str(product_id))

        self.product_tab.name_entry.delete(0, "end")
        self.product_tab.name_entry.insert(0, "Updated Product")

        self.product_tab.price_entry.delete(0, "end")
        self.product_tab.price_entry.insert(0, "75.50")

        # Reset refresh called flag
        self.refresh_called = False

        # Update product
        self.product_tab.update_product()

        # Check message
        self.assertEqual(
            self.message_label.cget("text"),
            f"Product ID {product_id} updated successfully.",
        )
        self.assertEqual(self.message_label.cget("text_color"), "#4BB543")

        # Check if refresh callback was called
        self.assertTrue(self.refresh_called)

        # Check if product was updated in database
        updated_product = self.db_manager.get_product_by_id(product_id)
        self.assertEqual(updated_product[1], "Updated Product")
        self.assertEqual(float(updated_product[2]), 75.50)

        # Check if form was cleared
        self.assertEqual(self.product_tab.id_entry.get(), "")
        self.assertEqual(self.product_tab.name_entry.get(), "")
        self.assertEqual(self.product_tab.price_entry.get(), "")

    def test_update_nonexistent_product(self):
        """Test update with non-existent product ID."""

        # Set form values for update with non-existent ID
        self.product_tab.id_entry.delete(0, "end")
        self.product_tab.id_entry.insert(0, "999")  # Non-existent ID

        self.product_tab.name_entry.delete(0, "end")
        self.product_tab.name_entry.insert(0, "Updated Product")

        self.product_tab.price_entry.delete(0, "end")
        self.product_tab.price_entry.insert(0, "75.50")

        # Update product
        self.product_tab.update_product()

        # Check error message
        self.assertEqual(
            self.message_label.cget("text"), "No product found with ID 999."
        )
        self.assertEqual(self.message_label.cget("text_color"), "#FF3333")

        # Check that refresh was not called
        self.assertFalse(self.refresh_called)

    def test_delete_product_success(self):
        """Test successful product deletion."""

        # Add a product to delete
        self.db_manager.add_product("Delete Me", "25.00")
        products = self.db_manager.get_all_products()
        product_id = products[0][0]

        # Set ID for deletion
        self.product_tab.id_entry.delete(0, "end")
        self.product_tab.id_entry.insert(0, str(product_id))

        # Reset refresh called flag
        self.refresh_called = False

        # Delete product
        self.product_tab.delete_product()

        # Check message
        self.assertEqual(
            self.message_label.cget("text"),
            f"Product ID {product_id} deleted successfully.",
        )
        self.assertEqual(self.message_label.cget("text_color"), "#4BB543")

        # Check if refresh callback was called
        self.assertTrue(self.refresh_called)

        # Check if product was deleted from database
        products_after = self.db_manager.get_all_products()
        self.assertEqual(len(products_after), 0)

        # Check if form was cleared
        self.assertEqual(self.product_tab.id_entry.get(), "")


if __name__ == "__main__":
    unittest.main()
