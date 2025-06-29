import os

import pytest

try:
    from src.ui.components import MessageLabel, StyledButton
    from src.ui.styles import AppStyles
except ImportError:
    pytest.skip("UI components not available", allow_module_level=True)

# Skip UI tests if running in headless environment
pytestmark = pytest.mark.skipif(
    os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true",
    reason="UI tests require display",
)


@pytest.mark.ui
class TestUIComponents:
    """Test UI components."""

    def test_message_label_show_success(self, message_label: MessageLabel) -> None:
        """Test MessageLabel success message display.

        Args:
            message_label (MessageLabel): The MessageLabel instance.
        """
        message_label.show_success("Success message")

        assert message_label.cget("text") == "Success message"
        assert message_label.cget("text_color") == "#4BB543"

    def test_message_label_show_error(self, message_label: MessageLabel) -> None:
        """Test MessageLabel error message display.

        Args:
            message_label (MessageLabel): The MessageLabel instance.
        """
        message_label.show_error("Error message")

        assert message_label.cget("text") == "Error message"
        assert message_label.cget("text_color") == "#FF3333"

    def test_message_label_show_info(self, message_label: MessageLabel) -> None:
        """Test MessageLabel info message display.

        Args:
            message_label (MessageLabel): The MessageLabel instance.
        """
        message_label.show_info("Info message")

        assert message_label.cget("text") == "Info message"
        assert message_label.cget("text_color") == "gray"

    def test_message_label_clear(self, message_label: MessageLabel) -> None:
        """Test MessageLabel clear method.

        Args:
            message_label (MessageLabel): The MessageLabel instance.
        """
        message_label.show_info("Some message")
        message_label.clear()

        assert message_label.cget("text") == ""

    def test_styled_button_primary(self, ui_frame) -> None:
        """Test StyledButton with primary style.

        Args:
            ui_frame (ctk.CTk): The UI frame instance.
        """
        button = StyledButton(ui_frame, text="Primary Button", button_type="primary")
        button.pack()

        assert button.cget("fg_color") == AppStyles.PRIMARY_COLOR
        assert button.cget("text") == "Primary Button"

    def test_styled_button_danger(self, ui_frame) -> None:
        """Test StyledButton with danger style.

        Args:
            ui_frame (ctk.CTk): The UI frame instance.
        """
        button = StyledButton(ui_frame, text="Danger Button", button_type="danger")
        button.pack()

        assert button.cget("fg_color") == AppStyles.DANGER_COLOR
        assert button.cget("text") == "Danger Button"

    def test_styled_button_success(self, ui_frame) -> None:
        """Test StyledButton with success style.

        Args:
            ui_frame (ctk.CTk): The UI frame instance.
        """
        button = StyledButton(ui_frame, text="Success Button", button_type="success")
        button.pack()

        assert button.cget("fg_color") == AppStyles.SUCCESS_COLOR
        assert button.cget("text") == "Success Button"

    @pytest.mark.parametrize(
        "button_type,expected_color",
        [
            ("primary", AppStyles.PRIMARY_COLOR),
            ("danger", AppStyles.DANGER_COLOR),
            ("success", AppStyles.SUCCESS_COLOR),
        ],
    )
    def test_styled_button_colors(self, ui_frame, button_type, expected_color) -> None:
        """Test StyledButton colors with parametrization.

        Args:
            ui_frame (ctk.CTk): The UI frame instance.
            button_type (str): The type of the button.
            expected_color (str): The expected foreground color.
        """
        button = StyledButton(ui_frame, text="Test Button", button_type=button_type)
        button.pack()

        assert button.cget("fg_color") == expected_color
