import customtkinter as ctk
from typing import Any, Dict, List, Tuple

from src.core.database import DatabaseManager
from .. import MessageLabel
from src.ui.styles import AppStyles
from .stats_section import StatsSection
from src.ui.components.stats_panel.categories_section import CategoriesSection


class StatisticsPanel:
    """Panel showing inventory statistics"""

    def __init__(
        self, parent: Any, db_manager: DatabaseManager, result_label: MessageLabel
    ) -> None:
        """Initialize the statistics panel.

        Args:
            parent (Any): The parent container for the statistics panel.
            db_manager (DatabaseManager): The database manager instance.
            result_label (MessageLabel): The label to display results or messages.
        """
        self.parent = parent
        self.db_manager = db_manager
        self.result_label = result_label

        self._create_panel()

    def _create_panel(self) -> None:
        """Create the statistics panel UI"""

        # Frame for summary section (Statistics)
        self.summary_frame = ctk.CTkFrame(self.parent)
        self.summary_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Section title
        summary_title = ctk.CTkLabel(
            self.summary_frame, text="Inventory Summary", font=AppStyles.HEADER_FONT
        )
        summary_title.pack(pady=(5, 10))

        # Container Dividend statistics into two columns
        main_container = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)

        # LEFT COLUMN: KEY STATISTICS
        self.stats_section = StatsSection(main_container)
        self.total_products_label = self.stats_section.total_products_label
        self.total_value_label = self.stats_section.total_value_label
        self.avg_price_label = self.stats_section.avg_price_label
        self.max_price_label = self.stats_section.max_price_label
        self.min_price_label = self.stats_section.min_price_label

        # RIGHT COLUMN: CATEGORIES
        self.categories_section = CategoriesSection(main_container)
        self.categories_frame = self.categories_section.categories_frame

    def update_stats(self) -> None:
        """Fetch product statistics from the database and update the UI labels and categories list."""

        try:
            stats: Dict[str, Any] = self.db_manager.get_product_stats()

            total: int = stats.get("total_products", 0)
            self.total_products_label.configure(text=str(total))

            if total == 0:

                # No products: clear or set placeholders
                self.total_value_label.configure(text="No products")
                self.avg_price_label.configure(text="N/A")
                self.max_price_label.configure(text="N/A")
                self.min_price_label.configure(text="N/A")

                # Clear categories
                for widget in self.categories_frame.winfo_children():
                    widget.destroy()

                empty_label = ctk.CTkLabel(
                    self.categories_frame,
                    text="No categories available",
                    font=AppStyles.NORMAL_FONT,
                )

                empty_label.pack(anchor="w", pady=10, padx=5)
                self.result_label.show_info("No products to show statistics.")

                return

            # Update statistics labels
            total_value: float = stats.get("total_value", 0.0) or 0.0
            self.total_value_label.configure(text=f"${total_value:,.2f}")

            # Average price
            avg_price: float = stats.get("avg_price", 0.0) or 0.0
            self.avg_price_label.configure(text=f"${avg_price:,.2f}")

            # Most and least expensive products
            max_prod: Tuple[Any, ...] = stats.get("max_price_product", ())
            max_name: str = max_prod[1] if len(max_prod) > 1 else "N/A"

            if len(max_name) > 15:
                max_name = max_name[:15] + "..."

            max_price_val: float = float(max_prod[2]) if len(max_prod) > 2 else 0.0
            self.max_price_label.configure(text=f"{max_name} (${max_price_val:,.2f})")

            # Least expensive product
            min_prod: Tuple[Any, ...] = stats.get("min_price_product", ())
            min_name: str = min_prod[1] if len(min_prod) > 1 else "N/A"

            if len(min_name) > 15:
                min_name = min_name[:15] + "..."

            min_price_val: float = float(min_prod[2]) if len(min_prod) > 2 else 0.0
            self.min_price_label.configure(text=f"{min_name} (${min_price_val:,.2f})")

            # Update categories list
            for widget in self.categories_frame.winfo_children():
                widget.destroy()

            categories: List[Tuple[Any, int]] = stats.get("categories", [])

            if not categories:
                empty_label = ctk.CTkLabel(
                    self.categories_frame,
                    text="No categories available",
                    font=AppStyles.NORMAL_FONT,
                )
                empty_label.pack(anchor="w", pady=10, padx=5)
            else:

                # Sort categories descending by count
                try:
                    categories.sort(key=lambda x: x[1], reverse=True)
                except Exception:
                    pass

                # Simple color list for indicators
                colors = [
                    "#3498db",
                    "#2ecc71",
                    "#e74c3c",
                    "#f39c12",
                    "#9b59b6",
                    "#1abc9c",
                    "#e67e22",
                    "#34495e",
                ]

                # Create category frames
                for i, (category, count) in enumerate(categories):
                    cat_frame = ctk.CTkFrame(
                        self.categories_frame, fg_color=("gray90", "gray25")
                    )
                    cat_frame.pack(fill="x", pady=2, padx=2, ipady=2)

                    color_ind = ctk.CTkFrame(
                        cat_frame, width=8, height=24, fg_color=colors[i % len(colors)]
                    )
                    color_ind.pack(side="left", padx=(2, 8))

                    cat_label = ctk.CTkLabel(
                        cat_frame,
                        text=f"{category}: {count} product{'s' if count != 1 else ''}",
                        font=AppStyles.NORMAL_FONT,
                        anchor="w",
                    )
                    cat_label.pack(side="left", fill="x", expand=True, padx=2)

            self.result_label.show_info("Statistics updated.")

        except Exception as e:
            self.result_label.show_error(f"Error loading statistics: {e}")
