import customtkinter as ctk
import os
from typing import Any
from src.core.database import DatabaseManager
from src.models.models import Employee
from src.ui.components.login import LoginFrame
from src.ui.components.inventory import InventoryFrame
from src.ui.styles import AppStyles


class InventoryApp:
    """
    Main controller for the Inventory application.
    Manages the initial login screen and, upon success, shows the inventory management UI.
    """

    def __init__(self) -> None:
        """
        Initialize the application: set up styles, database, and show login.
        """
        # Apply global styles
        AppStyles.setup()

        # Initialize database manager with a relative path. Adjust if your structure differs.
        self.db_path: str = os.path.join('src', 'db', 'inventory.db')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.db_manager: DatabaseManager = DatabaseManager(self.db_path)

        # Create main window
        self.app: ctk.CTk = ctk.CTk()
        self.app.title("Inventory System")
        
        # Set window size; adjust or allow resizing if needed
        self.app.geometry("600x700")
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
        self.current_frame = LoginFrame(self.app, self._on_login_success)

    def show_inventory(self, employee: Employee) -> None:
        """
        Clear current widgets and display the inventory management frame.\n
        param employee: Employee object after successful login
        """
        self._clear_app()
        
        # Create InventoryFrame and pack it
        self.current_frame = InventoryFrame(
            self.app,
            self.db_manager,
            employee,
            self.show_login  # callback for logout
        )
        self.current_frame.pack(padx=20, pady=20, fill="both", expand=True)

    def _clear_app(self) -> None:
        """
        Destroy all widgets currently in the main window.
        """
        for widget in self.app.winfo_children():
            widget.destroy()

    def _on_login_success(self, employee: Employee) -> None:
        """
        Callback invoked by LoginFrame when login succeeds.
        :param employee: Employee instance returned by login logic
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
