import customtkinter as ctk

from src.ui.styles import AppStyles


class MessageLabel(ctk.CTkLabel):
    """Label for showing status messages.

    Args:
        ctk (CTkLabel): The custom tkinter label.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the message label."""
        super().__init__(*args, **kwargs)
        self.configure(text="", text_color="gray")

    def show_success(self, message) -> None:
        """Display a success message.

        Args:
            message (str): The success message to display.
        """
        self.configure(text=message, text_color="#4BB543")

    def show_error(self, message) -> None:
        """Display an error message.

        Args:
            message (str): The error message to display.
        """
        self.configure(text=message, text_color="#FF3333")

    def show_info(self, message) -> None:
        """Display an informational message.

        Args:
            message (str): The informational message to display.
        """
        self.configure(text=message, text_color="gray")

    def clear(self) -> None:
        """Clear the message."""
        self.configure(text="")


class FormField:
    """Utility class to create standardized form fields."""

    @staticmethod
    def create_field(parent, label_text, placeholder="", **kwargs) -> ctk.CTkEntry:
        """Create a labeled form field.

        Args:
            parent (ctk.CTkFrame): The parent frame for the form field.
            label_text (str): The text to display as the field label.
            placeholder (str, optional): The placeholder text for the entry
                field. Defaults to "".

        Returns:
            ctk.CTkEntry: The created entry field.
        """
        container = ctk.CTkFrame(parent)
        container.pack(fill="x", padx=20, pady=5)

        label = ctk.CTkLabel(container, text=label_text, anchor="w")
        label.pack(fill="x")

        entry = ctk.CTkEntry(container, placeholder_text=placeholder, **kwargs)
        entry.pack(fill="x", pady=(0, 5))

        return entry


class StyledButton(ctk.CTkButton):
    """Button with predefined styles.

    Args:
        ctk (module): The custom tkinter module.
    """

    def __init__(self, *args, button_type="primary", **kwargs) -> None:
        """Initialize the styled button.

        Args:
            button_type (str, optional): The type of button to create.
                Defaults to "primary".
        """
        style = AppStyles.get_button_style(button_type)

        # Merge the style dict with kwargs
        for key, value in style.items():

            if key not in kwargs:
                kwargs[key] = value

        super().__init__(*args, **kwargs)
