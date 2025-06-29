import os
import sys
import tempfile

import pytest

try:
    import customtkinter as ctk

    from src.core.database import DatabaseManager
    from src.models.employee_model import Employee
    from src.models.product_model import Product
    from src.ui.components import MessageLabel
    from src.ui.styles import AppStyles

    UI_AVAILABLE = True
except ImportError as e:
    print(f"UI imports failed: {e}")
    UI_AVAILABLE = False

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Configure environment for headless testing
os.environ["PYTEST_RUNNING"] = "1"


@pytest.fixture(scope="session")
def setup_ui():
    """Setup the UI environment for testing.

    Yields:
        ctk.CTk: The root CTk instance.
    """
    if not UI_AVAILABLE:
        pytest.skip("UI components not available")

    try:
        # Try to create a root window in headless mode
        root = ctk.CTk()
        root.withdraw()  # Hide the window immediately
        AppStyles.setup()
        yield root
        root.quit()
        root.destroy()
    except Exception as e:
        pytest.skip(f"Cannot create UI environment: {e}")


@pytest.fixture
def temp_database():
    """Create a temporary database for testing.

    Yields:
        DatabaseManager: The database manager instance.
        str: The path to the temporary database file.
    """
    temp_fd, temp_path = tempfile.mkstemp()
    db_manager = DatabaseManager(temp_path)

    yield db_manager, temp_path

    # Cleanup
    if hasattr(db_manager, "conn") and db_manager.conn:
        db_manager.conn.close()
        db_manager.conn = None

    try:
        os.close(temp_fd)
    except OSError:
        pass

    try:
        os.unlink(temp_path)
    except (OSError, PermissionError) as e:
        print(f"Could not delete {temp_path}: {e}")


@pytest.fixture
def ui_frame(setup_ui):
    """Create a UI frame for testing.

    Args:
        setup_ui (ctk.CTk): The setup UI instance.

    Returns:
        ctk.CTkFrame: The created UI frame.

    Yields:
        Iterator[ctk.CTkFrame]: The created UI frame.
    """
    root = setup_ui
    frame = ctk.CTkFrame(root)
    frame.pack()
    yield frame
    frame.destroy()


@pytest.fixture
def message_label(ui_frame):
    """Create a message label for testing.

    Args:
        ui_frame (ctk.CTkFrame): The UI frame instance.

    Returns:
        MessageLabel: MessageLabel instance.
    """
    label = MessageLabel(ui_frame)
    label.pack()
    return label


@pytest.fixture
def sample_products():
    """Sample products for testing."""
    return [
        Product(id=1, name="Laptop XPS", price=1200.00),
        Product(id=2, name="Mouse Logitech", price=25.00),
        Product(id=3, name="Keyboard Mechanical", price=150.00),
    ]


@pytest.fixture
def sample_employees():
    """Sample employees for testing."""
    return [
        Employee(id="E001", name="John Doe", role="Admin"),
        Employee(id="E002", name="Javier Perez", role="Manager"),
        Employee(id="E003", name="Alex Rodriguez", role="Clerk"),
    ]
