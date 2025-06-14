import customtkinter as ctk
from typing import Any, Dict, List, Tuple

from src.core.database import DatabaseManager
from ..components import MessageLabel
from src.ui.styles import AppStyles


class StatisticsPanel:
    """Panel showing inventory statistics"""

    def __init__(
        self, parent: Any, db_manager: DatabaseManager, result_label: MessageLabel
    ) -> None:
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
        self._create_stats_section(main_container)

        # RIGHT COLUMN: CATEGORIES
        self._create_categories_section(main_container)

    def _create_stats_section(self, container: Any) -> None:
        """Create the key statistics section"""
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
        for i, label_text in enumerate(labels):
            lbl = ctk.CTkLabel(
                stats_grid, text=label_text, font=AppStyles.NORMAL_FONT, anchor="w"
            )
            lbl.grid(row=i, column=0, sticky="w", padx=5, pady=2)

        self.total_products_label = ctk.CTkLabel(
            stats_grid, text="Loading...", font=AppStyles.NORMAL_FONT
        )
        self.total_products_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        self.total_value_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.total_value_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        self.avg_price_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.avg_price_label.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        self.max_price_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.max_price_label.grid(row=3, column=1, sticky="w", padx=5, pady=2)
        self.min_price_label = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.min_price_label.grid(row=4, column=1, sticky="w", padx=5, pady=2)

    def _create_categories_section(self, container: Any) -> None:
        """Create the categories section"""
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

    def update_stats(self) -> None:
        """
        Fetch product statistics from the database and update the UI labels and categories list.
        """
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

            total_value: float = stats.get("total_value", 0.0) or 0.0
            self.total_value_label.configure(text=f"${total_value:,.2f}")

            avg_price: float = stats.get("avg_price", 0.0) or 0.0
            self.avg_price_label.configure(text=f"${avg_price:,.2f}")

            max_prod: Tuple[Any, ...] = stats.get("max_price_product", ())
            max_name: str = max_prod[1] if len(max_prod) > 1 else "N/A"
            if len(max_name) > 15:
                max_name = max_name[:15] + "..."
            max_price_val: float = float(max_prod[2]) if len(max_prod) > 2 else 0.0
            self.max_price_label.configure(text=f"{max_name} (${max_price_val:,.2f})")

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
