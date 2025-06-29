import os
import tempfile

import customtkinter as ctk
import pytest

from src.core.database import DatabaseManager
from src.ui.components.components import MessageLabel
from src.ui.components.stats_panel.stats_panel import StatisticsPanel
from src.ui.styles import AppStyles


@pytest.fixture(scope="module")
def root() -> ctk.CTk:
    """Fixture to create the root window for all tests in the module.

    Returns:
        ctk.CTk: The CustomTkinter root window.
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
    if hasattr(db_manager, "conn") and db_manager.conn:
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
def stats_panel(root: ctk.CTk, temp_db: DatabaseManager):
    """Fixture to create the statistics panel and its dependencies.

    Args:
        root (ctk.CTk): The root window.
        temp_db (DatabaseManager): Temporary database.

    Returns:
        tuple: (StatisticsPanel, MessageLabel, DatabaseManager)
    """
    frame = ctk.CTkFrame(root)
    frame.pack()
    message_label = MessageLabel(frame)
    message_label.pack()
    panel = StatisticsPanel(frame, temp_db, message_label)
    yield panel, message_label, temp_db
    frame.destroy()


def test_empty_statistics(stats_panel: tuple) -> None:
    """Test statistics display with no products in the database.

    Args:
        stats_panel (tuple): The statistics panel, message label, and database manager.
    """
    panel, message_label, db_manager = stats_panel
    panel.update_stats()
    assert panel.total_products_label.cget("text") == "0"
    assert panel.total_value_label.cget("text") == "No products"
    assert panel.avg_price_label.cget("text") == "N/A"
    assert panel.max_price_label.cget("text") == "N/A"
    assert panel.min_price_label.cget("text") == "N/A"
    assert message_label.cget("text") == "No products to show statistics."


def test_statistics_with_products(stats_panel: tuple) -> None:
    """Test statistics display with products in the database.

    Args:
        stats_panel (tuple): The statistics panel, message label, and database manager.
    """
    panel, message_label, db_manager = stats_panel
    db_manager.add_product("Laptop Dell", "1000.00")
    db_manager.add_product("Laptop HP", "800.00")
    db_manager.add_product("Mouse Logitech", "30.00")
    panel.update_stats()
    assert panel.total_products_label.cget("text") == "3"
    assert panel.total_value_label.cget("text") == "$1,830.00"
    assert panel.avg_price_label.cget("text") == "$610.00"
    assert "Laptop Dell" in panel.max_price_label.cget("text")
    assert "$1,000.00" in panel.max_price_label.cget("text")
    assert "Mouse Logitech" in panel.min_price_label.cget("text")
    assert "$30.00" in panel.min_price_label.cget("text")
    assert message_label.cget("text") == "Statistics updated."


def test_category_counting(stats_panel: tuple) -> None:
    """Test that categories are correctly counted and displayed.

    Args:
        stats_panel (tuple): The statistics panel, message label, and database manager.
    """
    panel, message_label, db_manager = stats_panel
    db_manager.add_product("Laptop Dell", "1000.00")
    db_manager.add_product("Laptop HP", "800.00")
    db_manager.add_product("Mouse Logitech", "30.00")
    db_manager.add_product("Mouse Microsoft", "25.00")
    db_manager.add_product("Keyboard Logitech", "50.00")
    panel.update_stats()
    stats = db_manager.get_product_stats()
    categories = {category: count for category, count in stats["categories"]}
    assert categories["Laptop"] == 2
    assert categories["Mouse"] == 2
    assert categories["Keyboard"] == 1
