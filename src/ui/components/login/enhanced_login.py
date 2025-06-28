import os
from typing import Any, Callable

import customtkinter as ctk
from PIL import Image

from src.models import Employee
from src.utils.password_utils import toggle_password_visibility
from src.utils.placeholder_illustration import create_placeholder_illustration


class EnhancedLoginUI(ctk.CTkFrame):
    """Enhanced login UI with a modern design.

    Args:
        ctk (module): The customtkinter module.
    """

    def __init__(self, master: Any, on_login_success: Callable[[Employee], None]):
        """
        Initialize the enhanced login UI.

        Args:
            master: The parent widget
            on_login_success: Callback function called on successful login
        """
        super().__init__(master, fg_color="#000000", corner_radius=0)
        self.pack(fill="both", expand=True)
        self.on_login_success = on_login_success
        self.show_password = False

        # Create the login UI with two panels
        self._create_login_ui()

    def _create_login_ui(self):
        """Create the two-panel login UI with illustration and form."""

        # Main container with two columns
        main_container = ctk.CTkFrame(self, fg_color="#0f0f11", corner_radius=20)
        main_container.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8
        )

        # Left panel - Illustration
        left_panel = ctk.CTkFrame(main_container, fg_color="#0f0f11", corner_radius=20)
        left_panel.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=20)

        # Right panel - Login form
        right_panel = ctk.CTkFrame(main_container, fg_color="#0f0f11", corner_radius=20)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=20)

        # Add illustration to left panel
        self._add_illustration(left_panel)

        # Add login form to right panel
        self._add_login_form(right_panel)

    def _add_illustration(self, panel: ctk.CTkFrame):
        """Add an illustration to the left panel of the login UI.

        Args:
            panel (ctk.CTkFrame): The left panel frame
        """

        # Try to load illustration image from assets folder
        try:
            img_path = os.path.join("assets", "login_img.webp")
            if os.path.exists(img_path):
                img = ctk.CTkImage(
                    light_image=Image.open(img_path),
                    dark_image=Image.open(img_path),
                    size=(300, 300),
                )
                illustration = ctk.CTkLabel(panel, image=img, text="")
                illustration.place(relx=0.5, rely=0.5, anchor="center")
            else:
                create_placeholder_illustration(panel)
        except Exception:
            create_placeholder_illustration(panel)

    def _add_login_form(self, panel: ctk.CTkFrame):
        """Add the login form to the right panel.

        Args:
            panel (ctk.CTkFrame): The right panel frame
        """

        # Welcome text
        welcome_label = ctk.CTkLabel(
            panel, text="WELCOME", font=("Roboto", 28, "bold"), text_color="white"
        )
        welcome_label.place(relx=0.5, rely=0.1, anchor="center")

        # Profile avatar circle
        avatar_frame = ctk.CTkFrame(
            panel, width=80, height=80, fg_color="#4285f4", corner_radius=40
        )
        avatar_frame.place(relx=0.5, rely=0.25, anchor="center")

        # User icon in the avatar
        user_icon = ctk.CTkLabel(
            avatar_frame, text="👤", font=("Roboto", 36), text_color="white"
        )
        user_icon.place(relx=0.5, rely=0.5, anchor="center")

        # Sign In text
        sign_in_label = ctk.CTkLabel(
            panel, text="Sign In", font=("Roboto", 18), text_color="white"
        )
        sign_in_label.place(relx=0.5, rely=0.35, anchor="center")

        # Username
        username_label = ctk.CTkLabel(
            panel, text="Username", font=("Roboto", 12), text_color="gray"
        )
        username_label.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.8)

        self.username_entry = ctk.CTkEntry(
            panel,
            placeholder_text="Enter your username",
            fg_color="#1a1a1c",
            border_color="#333333",
            text_color="white",
            corner_radius=5,
        )
        self.username_entry.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)

        # Password
        password_label = ctk.CTkLabel(
            panel, text="Password", font=("Roboto", 12), text_color="gray"
        )
        password_label.place(relx=0.5, rely=0.58, anchor="center", relwidth=0.8)

        self.password_entry = ctk.CTkEntry(
            panel,
            placeholder_text="Enter your password",
            fg_color="#1a1a1c",
            border_color="#333333",
            text_color="white",
            corner_radius=5,
            show="•",
        )
        self.password_entry.place(relx=0.5, rely=0.63, anchor="center", relwidth=0.8)

        # Show password icon
        show_password_icon = ctk.CTkButton(
            panel,
            text="👁",
            width=20,
            height=20,
            fg_color="#0f0f11",
            hover_color="#2a2a2c",
            command=self._toggle_password_visibility,
        )
        show_password_icon.place(relx=0.85, rely=0.63, anchor="center")

        # Login button
        self.login_button = ctk.CTkButton(
            panel,
            text="LOGIN",
            font=("Roboto", 14, "bold"),
            fg_color="#4285f4",
            hover_color="#2a75f3",
            corner_radius=5,
            command=self._handle_login,
        )
        self.login_button.place(
            relx=0.5, rely=0.72, anchor="center", relwidth=0.8, relheight=0.06
        )

        # Forgot password link
        self.forgot_password_link = ctk.CTkButton(
            panel,
            text="Forgot Password?",
            font=("Roboto", 12),
            fg_color="#0f0f11",
            hover_color="#1a1a1f",
            text_color="#4285f4",
            command=self._forgot_password,
        )
        self.forgot_password_link.place(relx=0.5, rely=0.8, anchor="center")

        # No account yet? text
        no_account_label = ctk.CTkLabel(
            panel, text="No account yet?", font=("Roboto", 12), text_color="gray"
        )
        no_account_label.place(relx=0.38, rely=0.88, anchor="center")

        # Sign up button
        self.sign_up_link = ctk.CTkButton(
            panel,
            text="Sign Up",
            font=("Roboto", 12, "bold"),
            fg_color="#0f0f11",
            hover_color="#1a1a1f",
            text_color="#4285f4",
            command=self._sign_up,
        )
        self.sign_up_link.place(relx=0.62, rely=0.88, anchor="center")

        # Error message label
        self.error_label = ctk.CTkLabel(
            panel, text="", font=("Roboto", 12), text_color="#FF3333"
        )
        self.error_label.place(relx=0.5, rely=0.94, anchor="center")

    def _handle_login(self):
        """Handle login button click."""

        emp_id = self.username_entry.get().strip()
        emp_name = "Administrator" if emp_id == "admin" else emp_id
        emp_role = "Admin" if emp_id == "admin" else "User"

        if not emp_id or not self.password_entry.get().strip():
            self.error_label.configure(text="Please enter both username and password")
            return

        # Create employee object - in a real app, you would validate against a database
        employee = Employee(id=f"E{len(emp_id):03d}", name=emp_name, role=emp_role)

        # Call the success callback
        self.on_login_success(employee)

    def _toggle_password_visibility(self):
        """Toggle password visibility using utility function."""
        self.show_password = toggle_password_visibility(
            self.password_entry, self.show_password
        )

    def _forgot_password(self):
        """Handle forgot password click."""
        self.error_label.configure(
            text="Please contact system administrator to reset your password",
            text_color="#4285f4",
        )

    def _sign_up(self):
        """Handle sign up click."""
        self.error_label.configure(
            text="Please contact system administrator for a new account",
            text_color="#4285f4",
        )
