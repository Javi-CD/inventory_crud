import customtkinter as ctk


def create_placeholder_illustration(panel: ctk.CTkFrame):
    """Create a placeholder illustration when image is not available.

    Args:
        panel (ctk.CTkFrame): The panel to place the illustration in.
    """

    # Create a placeholder frame with programmer illustration style
    illustration_placeholder = ctk.CTkFrame(
        panel, fg_color="#131418", corner_radius=10, width=300, height=300
    )
    illustration_placeholder.place(relx=0.5, rely=0.5, anchor="center")

    # Add some decorative elements to simulate the illustration
    desk = ctk.CTkFrame(
        illustration_placeholder,
        fg_color="#1a1a1f",
        corner_radius=5,
        width=250,
        height=100,
    )
    desk.place(relx=0.5, rely=0.7, anchor="center")

    monitor = ctk.CTkFrame(
        illustration_placeholder,
        fg_color="#00b8d4",
        corner_radius=5,
        width=120,
        height=80,
    )
    monitor.place(relx=0.5, rely=0.45, anchor="center")

    # Monitor screen
    screen = ctk.CTkFrame(
        monitor, fg_color="#1a1a1f", corner_radius=2, width=110, height=70
    )
    screen.place(relx=0.5, rely=0.5, anchor="center")

    # Person
    person = ctk.CTkLabel(
        illustration_placeholder,
        text="👨‍💻",
        font=("Roboto", 36),
        text_color="#00b8d4",
    )
    person.place(relx=0.5, rely=0.6, anchor="center")

    # Decorative elements
    gear1 = ctk.CTkLabel(
        illustration_placeholder,
        text="⚙️",
        font=("Roboto", 36),
        text_color="#00b8d4",
    )
    gear1.place(relx=0.2, rely=0.2)

    gear2 = ctk.CTkLabel(
        illustration_placeholder,
        text="⚙️",
        font=("Roboto", 24),
        text_color="#00b8d4",
    )
    gear2.place(relx=0.3, rely=0.15)

    lightbulb = ctk.CTkLabel(
        illustration_placeholder,
        text="💡",
        font=("Roboto", 36),
        text_color="#00b8d4",
    )
    lightbulb.place(relx=0.15, rely=0.3)

    # Title for illustration
    title = ctk.CTkLabel(
        panel,
        text="Inventory System",
        font=("Roboto", 18, "bold"),
        text_color="#00b8d4",
    )
    title.place(relx=0.5, rely=0.15, anchor="center")
