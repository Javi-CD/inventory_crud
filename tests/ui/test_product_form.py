import os
import tempfile

import customtkinter as ctk
import pytest

from src.core.database import DatabaseManager
from src.ui.components.components import MessageLabel
from src.ui.components.product.product_form import ProductManagementTab
from src.ui.styles import AppStyles


@pytest.fixture(scope="module")
def root() -> ctk.CTk:
    """Fixture to create the Root of the app once per module.

    Returns:
        ctk.CTk: Customtkinter root window.
    """
    root = ctk.CTk()
    AppStyles.setup()
    yield root
    root.destroy()


@pytest.fixture()
def temp_db() -> DatabaseManager:
    """Fixture to create a temporary database for each test.

    Returns:
        DatabaseManager: Instance of the temporary database.
    """
    temp_fd, temp_path = tempfile.mkstemp()
    db_manager = DatabaseManager(temp_path)
    yield db_manager
    if hasattr(db_manager, "Conn") and db_manager.conn:
        db_manager.conn.close()
        db_manager.conn = None
    try:
        os.close(temp_fd)
    except OSError:
        pass
    try:
        os.unlink(temp_path)
    except (OSError, PermissionError):
        pass


@pytest.fixture()
def product_tab(root: ctk.CTk, temp_db: DatabaseManager):
    """Fixture to create the product management form and its dependencies.

    ARGS:
        root (ctk.ctk): root window.
        Temp_DB (DatabaseManager): Temporary database.

    Returns:
        TUPLE: (ProductManogementtab, Messagelabel, Refresh_Called: List)
    """
    frame = ctk.CTkFrame(root)
    frame.pack()
    message_label = MessageLabel(frame)
    message_label.pack()
    refresh_called = []

    def refresh_callback():
        refresh_called.append(True)

    # Dummy switch_to_inventory_tab function
    def switch_to_inventory_tab():
        pass

    product_tab = ProductManagementTab(
        frame, temp_db, message_label, refresh_callback, switch_to_inventory_tab
    )
    yield product_tab, message_label, refresh_called, temp_db
    frame.destroy()


def test_create_product_success(product_tab):
    """Testa the successful creation of a product.

    ARGS:
        Product_tab (tuple): Fixtures of the form, label and callback.
    """
    tab, message_label, refresh_called, db_manager = product_tab

    # Set form values
    tab.name_entry.delete(0, "end")
    tab.name_entry.insert(0, "Test Product")

    tab.price_entry.delete(0, "end")
    tab.price_entry.insert(0, "99.99")

    # Create product
    tab.create_product()

    # Check message
    assert message_label.cget("text") == "Product 'Test Product' added successfully."
    assert message_label.cget("text_color") == "#4BB543"

    # Check if refresh callback was called
    assert refresh_called

    # Check if product was added to database
    products = db_manager.get_all_products()
    assert len(products) == 1
    assert products[0][1] == "Test Product"
    assert float(products[0][2]) == 99.99

    # Check if form was cleared
    assert tab.name_entry.get() == ""
    assert tab.price_entry.get() == ""


def test_create_product_missing_fields(product_tab):
    """Testa the creation of product with empty fields.

    ARGS:
        Product_tab (tuple): Fixtures of the form, label and callback.
    """
    tab, message_label, refresh_called, db_manager = product_tab

    # Clear form
    tab.name_entry.delete(0, "end")
    tab.price_entry.delete(0, "end")

    # Attempt to create product
    tab.create_product()

    # Check error message
    assert message_label.cget("text") == "Please complete all fields."
    assert message_label.cget("text_color") == "#FF3333"

    # Check that refresh was not called and no product was added
    assert not refresh_called
    products = db_manager.get_all_products()
    assert len(products) == 0


def test_create_product_invalid_price(product_tab):
    """Testa the creation of product with invalid price.

    ARGS:
        Product_tab (tuple): Fixtures of the form, label and callback.
    """
    tab, message_label, refresh_called, db_manager = product_tab

    # Set form values with invalid price
    tab.name_entry.delete(0, "end")
    tab.name_entry.insert(0, "Test Product")

    tab.price_entry.delete(0, "end")
    tab.price_entry.insert(0, "not-a-number")

    # Attempt to create product
    tab.create_product()

    # Check error message
    assert message_label.cget("text") == "Price must be numeric."
    assert message_label.cget("text_color") == "#FF3333"

    # Check that refresh was not called and no product was added
    assert not refresh_called
    products = db_manager.get_all_products()
    assert len(products) == 0


def test_update_product_success(product_tab):
    """Testa the successful update of a product.

    ARGS:
        Product_tab (tuple): Fixtures of the form, label and callback.
    """
    tab, message_label, refresh_called, db_manager = product_tab

    # Add a product to update
    db_manager.add_product("Original Product", "50.00")
    products = db_manager.get_all_products()
    product_id = products[0][0]

    # Set form values for update
    tab.id_entry.delete(0, "end")
    tab.id_entry.insert(0, str(product_id))

    tab.name_entry.delete(0, "end")
    tab.name_entry.insert(0, "Updated Product")

    tab.price_entry.delete(0, "end")
    tab.price_entry.insert(0, "75.50")

    # Reset refresh called flag
    refresh_called.clear()

    # Update product
    tab.update_product()

    # Check message
    assert (
        message_label.cget("text") == f"Product ID {product_id} updated successfully."
    )
    assert message_label.cget("text_color") == "#4BB543"

    # Check if refresh callback was called
    assert refresh_called

    # Check if product was updated in database
    updated_product = db_manager.get_product_by_id(product_id)
    assert updated_product[1] == "Updated Product"
    assert float(updated_product[2]) == 75.50

    # Check if form was cleared
    assert tab.id_entry.get() == ""
    assert tab.name_entry.get() == ""
    assert tab.price_entry.get() == ""


def test_update_nonexistent_product(product_tab):
    """Test the update of a non -existent product.

    ARGS:
        Product_tab (tuple): Fixtures of the form, label and callback.
    """
    tab, message_label, refresh_called, db_manager = product_tab

    # Set form values for update with non-existent ID
    tab.id_entry.delete(0, "end")
    tab.id_entry.insert(0, "999")  # Non-existent ID

    tab.name_entry.delete(0, "end")
    tab.name_entry.insert(0, "Updated Product")

    tab.price_entry.delete(0, "end")
    tab.price_entry.insert(0, "75.50")

    # Update product
    tab.update_product()

    # Check error message
    assert message_label.cget("text") == "No product found with ID 999."
    assert message_label.cget("text_color") == "#FF3333"

    # Check that refresh was not called
    assert not refresh_called


def test_delete_product_success(product_tab):
    """Testa the successful deletion of a product.

    ARGS:
        Product_tab (tuple): Fixtures of the form, label and callback.
    """
    tab, message_label, refresh_called, db_manager = product_tab

    # Add a product to delete
    db_manager.add_product("Delete Me", "25.00")
    products = db_manager.get_all_products()
    product_id = products[0][0]

    # Set ID for deletion
    tab.id_entry.delete(0, "end")
    tab.id_entry.insert(0, str(product_id))

    # Reset refresh called flag
    refresh_called.clear()

    # Delete product
    tab.delete_product()

    # Check message
    assert (
        message_label.cget("text") == f"Product ID {product_id} deleted successfully."
    )
    assert message_label.cget("text_color") == "#4BB543"

    # Check if refresh callback was called
    assert refresh_called

    # Check if product was deleted from database
    products_after = db_manager.get_all_products()
    assert len(products_after) == 0

    # Check if form was cleared
    assert tab.id_entry.get() == ""
