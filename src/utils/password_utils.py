def toggle_password_visibility(entry_widget, show_password: bool):
    """
    Toggle the visibility of a password entry widget.

    Args:
        entry_widget: The password entry widget (e.g., CTkEntry)
        show_password (bool): Current state of password visibility
    Returns:
        bool: The new state of password visibility
    """
    show_password = not show_password

    if show_password:
        entry_widget.configure(show="")
    else:
        entry_widget.configure(show="•")

    return show_password
