import os
from typing import Any

import customtkinter as ctk

from src.core.database import DatabaseManager
from src.models import Employee
from src.ui.components.inventory.inventory_frame import InventoryFrame
from src.ui.components.login.enhanced_login import EnhancedLoginUI
from src.ui.styles import AppStyles


class InventoryApp:
    """
    Main controller for the Inventory application.
    Manages the initial login screen and, upon success, shows the inventory
    management UI.
    """

    # Define db_path as a class attribute
    db_path: str = os.path.join("src", "db", "inventory.db")

    def __init__(self) -> None:
        """
        Initialize the application: set up styles, database, and show login.
        """
        # Apply global styles
        AppStyles.setup()

        # Initialize database manager
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.db_manager: DatabaseManager = DatabaseManager(self.db_path)

        # Create main window
        self.app: ctk.CTk = ctk.CTk()
        self.app.title("Inventory System")

        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        # Set window size; adjust or allow resizing if needed
        self.app.geometry(f"{screen_width}x{screen_height}+0+0")

        # Activate full screen mode
        # self.app.attributes("-fullscreen", True)

        self.app.resizable(False, False)

        # Keep reference to current frame
        self.current_frame: Any = None

        # Show login screen first
        self.show_login()

    def show_login(self) -> None:
        """
        Clear current widgets and display the login frame.
        """
        self._clear_app()

        # LoginFrame(master, on_success_callback)
        self.current_frame = EnhancedLoginUI(self.app, self._on_login_success)

    def show_inventory(self, employee: Employee) -> None:
        """Show the inventory management frame.

        Args:
            employee (Employee): The employee object after successful login.
        """
        self._clear_app()

        # Create InventoryFrame and pack it
        self.current_frame = InventoryFrame(
            self.app, self.db_manager, employee, self.show_login  # callback for logout
        )
        self.current_frame.pack(padx=20, pady=20, fill="both", expand=True)

    def _clear_app(self) -> None:
        """
        Destroy all widgets currently in the main window.
        """
        for widget in self.app.winfo_children():
            widget.destroy()

    def _on_login_success(self, employee: Employee) -> None:
        """Handle successful login.

        Args:
            employee (Employee): The employee object after successful login.
        """
        self.show_inventory(employee)

    def run(self) -> None:
        """
        Start the Tkinter main loop.
        """
        self.app.mainloop()


if __name__ == "__main__":
    app = InventoryApp()
    app.run()
