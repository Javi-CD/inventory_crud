import customtkinter as ctk
from typing import Any, Callable

from src.core.database import DatabaseManager
from src.models import Employee
from .. import MessageLabel, StyledButton
from src.ui.styles import AppStyles
from ..product.product_form import ProductManagementTab
from ..product.product_table import InventoryTab


class InventoryFrame(ctk.CTkFrame):
    """
    Frame for inventory management: provides two tabs—
    1) Product Management (CRUD)
    2) Inventory View (table + statistics)
    """

    def __init__(
        self,
        master: Any,
        db_manager: DatabaseManager,
        employee: Employee,
        on_logout: Callable[[], None],
    ) -> None:
        """
        Initialize InventoryFrame.

        Args:
            master (Any): Parent widget.
            db_manager (DatabaseManager): Instance of DatabaseManager.
            employee (Employee): Logged-in Employee instance.
            on_logout (Callable[[], None]): Callback to invoke when user logs out.
        """
        super().__init__(master)
        self.db_manager: DatabaseManager = db_manager
        self.employee: Employee = employee
        self.on_logout: Callable[[], None] = on_logout

        # Create widgets: header, message label, tabs, logout button
        self._create_widgets()

    def _create_widgets(self) -> None:
        """
        Create header, message label, tabbed interface, and logout button.
        """
        # Header with employee info
        self._create_header()

        # Message label to show feedback (errors/success/info)
        self.result_label: MessageLabel = MessageLabel(self)
        self.result_label.pack(pady=5)

        # Tabbed interface for CRUD and Inventory view
        self._create_tabbed_interface()

        # Logout button
        logout_btn = StyledButton(
            self, text="Logout", command=self.on_logout, button_type="neutral"
        )
        logout_btn.pack(pady=10)

    def _create_header(self) -> None:
        """
        Create header section with title and user info.
        """
        title = ctk.CTkLabel(
            self,
            text=f"Inventory Management - {self.employee.name}",
            font=AppStyles.TITLE_FONT,
        )
        title.pack(pady=15)

        emp_info = ctk.CTkLabel(
            self,
            text=f"User ID: {self.employee.id} | Role: {self.employee.role}",
            font=AppStyles.NORMAL_FONT,
        )
        emp_info.pack(pady=(0, 10))

    def _create_tabbed_interface(self) -> None:
        """
        Set up CTkTabview with two tabs: 'Product Management' and 'Inventory'.
        """
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Optional subtitle
        main_title = ctk.CTkLabel(
            main_frame, text="Inventory System", font=AppStyles.HEADER_FONT
        )
        main_title.pack(padx=15, pady=(0, 5))

        # Create the tab view
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)

        # Add two tabs
        self.tabview.add("Product Management")
        self.tabview.add("Inventory")  # Create product management tab
        self.product_tab = ProductManagementTab(
            self.tabview.tab("Product Management"),
            self.db_manager,
            self.result_label,
            self.refresh_data,
            self.switch_to_inventory_tab,  # Pass callback to switch to inventory tab
        )

        # Create inventory tab
        self.inventory_tab = InventoryTab(
            self.tabview.tab("Inventory"), self.db_manager, self.result_label
        )

        # Initial load of products and statistics
        self.refresh_data()

    def refresh_data(self) -> None:
        """Refresh all data in both tabs"""
        self.inventory_tab.read_products()
        self.inventory_tab.update_summary_data()

    def switch_to_inventory_tab(self) -> None:
        """Change to the Inventory tab after product operations"""
        self.tabview.set("Inventory")  # Switch to the Inventory tab
