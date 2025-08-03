from typing import Any

import customtkinter as ctk

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
        stats_frame = self._create_main_frame(container)
        self._add_section_title(stats_frame)
        stats_grid = self._create_stats_grid(stats_frame)
        self._create_label_headers(stats_grid)
        self._create_value_labels(stats_grid)

    def _create_main_frame(self, container: Any) -> ctk.CTkFrame:
        """Create and configure the main statistics frame.
        
        Args:
            container (Any): The parent container for the frame.
            
        Returns:
            ctk.CTkFrame: The configured main frame.
        """
        stats_frame = ctk.CTkFrame(container)
        stats_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        return stats_frame

    def _add_section_title(self, stats_frame: ctk.CTkFrame) -> None:
        """Add the section title to the statistics frame.
        
        Args:
            stats_frame (ctk.CTkFrame): The frame to add the title to.
        """
        stats_title = ctk.CTkLabel(
            stats_frame, text="Key Statistics", font=AppStyles.NORMAL_FONT
        )
        stats_title.pack(anchor="w", padx=10, pady=(5, 5))

    def _create_stats_grid(self, stats_frame: ctk.CTkFrame) -> ctk.CTkFrame:
        """Create and configure the grid container for statistics.
        
        Args:
            stats_frame (ctk.CTkFrame): The parent frame for the grid.
            
        Returns:
            ctk.CTkFrame: The configured grid frame.
        """
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="both", expand=True, padx=10, pady=5)
        return stats_grid

    def _create_label_headers(self, stats_grid: ctk.CTkFrame) -> None:
        """Create the header labels for each statistic.
        
        Args:
            stats_grid (ctk.CTkFrame): The grid frame to add labels to.
        """
        labels = self._get_statistic_labels()
        
        for i, label_text in enumerate(labels):
            lbl = ctk.CTkLabel(
                stats_grid, text=label_text, font=AppStyles.NORMAL_FONT, anchor="w"
            )
            lbl.grid(row=i, column=0, sticky="w", padx=5, pady=2)

    def _get_statistic_labels(self) -> list[str]:
        """Get the list of statistic label texts.
        
        Returns:
            list[str]: List of label texts for statistics.
        """
        return [
            "Total Products:",
            "Total Value:",
            "Average Price:",
            "Most Expensive Product:",
            "Least Expensive Product:",
        ]

    def _create_value_labels(self, stats_grid: ctk.CTkFrame) -> None:
        """Create all value display labels for statistics.
        
        Args:
            stats_grid (ctk.CTkFrame): The grid frame to add value labels to.
        """
        self._create_total_products_label(stats_grid)
        self._create_total_value_label(stats_grid)
        self._create_avg_price_label(stats_grid)
        self._create_max_price_label(stats_grid)
        self._create_min_price_label(stats_grid)

    def _create_total_products_label(self, stats_grid: ctk.CTkFrame) -> None:
        """Create the total products value label.
        
        Args:
            stats_grid (ctk.CTkFrame): The grid frame to add the label to.
        """
        self.total_products_label = ctk.CTkLabel(
            stats_grid, text="Loading...", font=AppStyles.NORMAL_FONT
        )
        self.total_products_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)

    def _create_total_value_label(self, stats_grid: ctk.CTkFrame) -> None:
        """Create the total value label.
        
        Args:
            stats_grid (ctk.CTkFrame): The grid frame to add the label to.
        """
        self.total_value_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.total_value_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)

    def _create_avg_price_label(self, stats_grid: ctk.CTkFrame) -> None:
        """Create the average price label.
        
        Args:
            stats_grid (ctk.CTkFrame): The grid frame to add the label to.
        """
        self.avg_price_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.avg_price_label.grid(row=2, column=1, sticky="w", padx=5, pady=2)

    def _create_max_price_label(self, stats_grid: ctk.CTkFrame) -> None:
        """Create the most expensive product label.
        
        Args:
            stats_grid (ctk.CTkFrame): The grid frame to add the label to.
        """
        self.max_price_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.max_price_label.grid(row=3, column=1, sticky="w", padx=5, pady=2)

    def _create_min_price_label(self, stats_grid: ctk.CTkFrame) -> None:
        """Create the least expensive product label.
        
        Args:
            stats_grid (ctk.CTkFrame): The grid frame to add the label to.
        """
        self.min_price_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.min_price_label.grid(row=4, column=1, sticky="w", padx=5, pady=2)
