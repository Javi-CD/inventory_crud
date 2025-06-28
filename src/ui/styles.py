import customtkinter as ctk


class AppStyles:
    """Centralized application styling."""

    # Colors
    PRIMARY_COLOR = "#1f538d"
    DANGER_COLOR = "#c42b2b"
    SUCCESS_COLOR = "#2b8a3e"
    WARNING_COLOR = "#e67700"

    # Fonts
    TITLE_FONT = ("Roboto", 24, "bold")
    HEADER_FONT = ("Roboto", 18, "bold")
    NORMAL_FONT = ("Roboto", 14)

    @classmethod
    def setup(cls):
        """Configure global application styles."""

        # Global configuration
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    @classmethod
    def get_button_style(cls, button_type="primary"):
        """Get button styling based on type.

        Args:
            button_type (str, optional): The type of button to style.
            Defaults to "primary".

        Returns:
            dict: A dictionary containing the button's foreground color and font.
        """

        styles = {
            "primary": {"fg_color": cls.PRIMARY_COLOR, "font": cls.NORMAL_FONT},
            "success": {"fg_color": cls.SUCCESS_COLOR, "font": cls.NORMAL_FONT},
            "danger": {"fg_color": cls.DANGER_COLOR, "font": cls.NORMAL_FONT},
            "warning": {"fg_color": cls.WARNING_COLOR, "font": cls.NORMAL_FONT},
            "neutral": {
                "fg_color": "gray25",
                "hover_color": "gray40",
                "font": cls.NORMAL_FONT,
            },
        }
        return styles.get(button_type, styles["primary"])
