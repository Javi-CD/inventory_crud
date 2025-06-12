import unittest
import tkinter as tk
import customtkinter as ctk
from src.ui.components.components import MessageLabel, StyledButton
from src.ui.styles import AppStyles


class TestUIComponents(unittest.TestCase):
    """Test UI component functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests."""
        cls.root = ctk.CTk()
        AppStyles.setup()

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        cls.root.destroy()

    def setUp(self):
        """Set up before each test."""
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack()

    def tearDown(self):
        """Clean up after each test."""
        self.frame.destroy()

    def test_message_label_show_success(self):
        """Test MessageLabel success message display."""
        message_label = MessageLabel(self.frame)
        message_label.pack()

        message_label.show_success("Success message")

        self.assertEqual(message_label.cget("text"), "Success message")
        self.assertEqual(message_label.cget("text_color"), "#4BB543")

    def test_message_label_show_error(self):
        """Test MessageLabel error message display."""
        message_label = MessageLabel(self.frame)
        message_label.pack()

        message_label.show_error("Error message")

        self.assertEqual(message_label.cget("text"), "Error message")
        self.assertEqual(message_label.cget("text_color"), "#FF3333")

    def test_message_label_show_info(self):
        """Test MessageLabel info message display."""
        message_label = MessageLabel(self.frame)
        message_label.pack()

        message_label.show_info("Info message")

        self.assertEqual(message_label.cget("text"), "Info message")
        self.assertEqual(message_label.cget("text_color"), "gray")

    def test_message_label_clear(self):
        """Test MessageLabel clear method."""
        message_label = MessageLabel(self.frame)
        message_label.pack()

        message_label.show_info("Some message")
        message_label.clear()

        self.assertEqual(message_label.cget("text"), "")

    def test_styled_button_primary(self):
        """Test StyledButton with primary style."""
        button = StyledButton(self.frame, text="Primary Button", button_type="primary")
        button.pack()

        self.assertEqual(button.cget("fg_color"), AppStyles.PRIMARY_COLOR)
        self.assertEqual(button.cget("text"), "Primary Button")

    def test_styled_button_danger(self):
        """Test StyledButton with danger style."""
        button = StyledButton(self.frame, text="Danger Button", button_type="danger")
        button.pack()

        self.assertEqual(button.cget("fg_color"), AppStyles.DANGER_COLOR)
        self.assertEqual(button.cget("text"), "Danger Button")

    def test_styled_button_success(self):
        """Test StyledButton with success style."""
        button = StyledButton(self.frame, text="Success Button", button_type="success")
        button.pack()

        self.assertEqual(button.cget("fg_color"), AppStyles.SUCCESS_COLOR)
        self.assertEqual(button.cget("text"), "Success Button")


if __name__ == "__main__":
    unittest.main()
