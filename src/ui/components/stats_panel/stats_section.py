import customtkinter as ctk
from typing import Any
from src.ui.styles import AppStyles


class StatsSection:
    """Section displaying key statistics about the inventory."""

    def __init__(self, parent: Any):
        """Initialize the statistics section.

        Args:
            parent (Any): The parent container for the statistics section.
        """
        self.parent = parent
        self._create_stats_section(parent)

    def _create_stats_section(self, container: Any) -> None:
        """Create the key statistics section.

        Args:
            container (Any): The parent container for the statistics section.
        """
        stats_frame = ctk.CTkFrame(container)
        stats_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        stats_title = ctk.CTkLabel(
            stats_frame, text="Key Statistics", font=AppStyles.NORMAL_FONT
        )
        stats_title.pack(anchor="w", padx=10, pady=(5, 5))

        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="both", expand=True, padx=10, pady=5)

        labels = [
            "Total Products:",
            "Total Value:",
            "Average Price:",
            "Most Expensive Product:",
            "Least Expensive Product:",
        ]

        # Create labels for each statistic
        for i, label_text in enumerate(labels):
            lbl = ctk.CTkLabel(
                stats_grid, text=label_text, font=AppStyles.NORMAL_FONT, anchor="w"
            )
            lbl.grid(row=i, column=0, sticky="w", padx=5, pady=2)

        # ------------------ Create labels to display the statistics ----------------- #

        # Total Products
        self.total_products_label = ctk.CTkLabel(
            stats_grid, text="Loading...", font=AppStyles.NORMAL_FONT
        )
        self.total_products_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        # Total Value
        self.total_value_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.total_value_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        # Average Price
        self.avg_price_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.avg_price_label.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        # Most Expensive Product
        self.max_price_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.max_price_label.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        # Least Expensive Product
        self.min_price_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.min_price_label.grid(row=4, column=1, sticky="w", padx=5, pady=2)
