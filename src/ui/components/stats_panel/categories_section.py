import customtkinter as ctk
from typing import Any
from src.ui.styles import AppStyles


class CategoriesSection:
    """Section displaying product categories."""

    def __init__(self, parent: Any):
        """Create the categories section.

        Args:
            parent (Any): The parent container for the categories section.
        """

        self.parent = parent
        self._create_categories_section(parent)

    def _create_categories_section(self, container: Any) -> None:
        """Create the categories section

        Args:
            container (Any): The parent container for the categories section.
        """

        categories_container = ctk.CTkFrame(container)
        categories_container.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        categories_title = ctk.CTkLabel(
            categories_container, text="Product Categories", font=AppStyles.NORMAL_FONT
        )
        categories_title.pack(anchor="w", padx=10, pady=(5, 5))

        categories_scroll = ctk.CTkScrollableFrame(
            categories_container, width=200, height=150
        )
        categories_scroll.pack(fill="both", expand=True, padx=10, pady=5)
        self.categories_frame = categories_scroll
