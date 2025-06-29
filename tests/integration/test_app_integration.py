import os
import tempfile

import pytest

from src.core.database import DatabaseManager
from src.models import Employee
from src.ui.app import InventoryApp


@pytest.fixture()
def temp_db_path():
    """Fixture to create a temporary database file path."""
    temp_fd, temp_path = tempfile.mkstemp()
    yield temp_path
    try:
        os.close(temp_fd)
    except OSError:
        pass
    try:
        os.unlink(temp_path)
    except (OSError, PermissionError):
        pass


@pytest.fixture()
def patch_db_path(temp_db_path):
    """Fixture to patch InventoryApp.db_path for the test duration."""
    old_db_path = InventoryApp.db_path
    InventoryApp.db_path = temp_db_path
    yield
    InventoryApp.db_path = old_db_path


def test_login_flow(monkeypatch):
    """Test the login functionality flow."""
    app = InventoryApp()
    # Track what frames are displayed
    state = {}

    def show_inventory(self, employee):
        state["current_frame"] = "inventory"
        state["test_employee"] = employee

    monkeypatch.setattr(InventoryApp, "show_inventory", show_inventory.__get__(app))
    app._on_login_success(Employee(id="E001", name="Test User", role="Admin"))
    assert state["current_frame"] == "inventory"
    assert state["test_employee"].id == "E001"
    assert state["test_employee"].name == "Test User"
    assert state["test_employee"].role == "Admin"


def test_database_integration(patch_db_path, temp_db_path):
    """Test that the app correctly integrates with the database."""
    db = DatabaseManager(temp_db_path)
    db.add_product("Test Product 1", "100.50")
    db.add_product("Test Product 2", "200.75")
    products = db.get_all_products()
    assert len(products) == 2
    assert products[0][1] == "Test Product 2"  # Due to ORDER BY name DESC
    assert float(products[0][2]) == 200.75
    assert products[1][1] == "Test Product 1"
    assert float(products[1][2]) == 100.50
    stats = db.get_product_stats()
    assert stats["total_products"] == 2
    assert float(stats["total_value"]) == 301.25
    assert float(stats["avg_price"]) == 150.625
    assert stats["max_price_product"][1] == "Test Product 2"
    assert float(stats["max_price_product"][2]) == 200.75


def test_app_initialization(patch_db_path, temp_db_path):
    """Test that the app initializes correctly."""
    app = InventoryApp()
    assert app.app.title() == "Inventory System"
    login_frame = None
    for widget in app.app.winfo_children():
        if "EnhancedLoginUI" in str(type(widget)):
            login_frame = widget
            break
    assert login_frame is not None
