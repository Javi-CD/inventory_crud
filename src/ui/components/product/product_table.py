import customtkinter as ctk
from typing import Any, Dict, List, Tuple

from src.core.database import DatabaseManager
from .. import MessageLabel, StyledButton
from src.ui.styles import AppStyles
from ..stats_panel.stats_panel import StatisticsPanel


class InventoryTab:
    """Tab for viewing inventory products in a table and showing statistics."""

    def __init__(
        self, parent: Any, db_manager: DatabaseManager, result_label: MessageLabel
    ) -> None:
        self.parent = parent
        self.db_manager = db_manager
        self.result_label = result_label

        self._create_table()
        self.stats_panel = StatisticsPanel(
            self.parent, self.db_manager, self.result_label
        )
        self._create_refresh_button()

    def _create_table(self) -> None:
        """Create the product table view"""

        # Container Frame for the table
        table_container = ctk.CTkFrame(self.parent)
        table_container.pack(padx=10, pady=10, fill="both", expand=True)

        self.table_scrollable = ctk.CTkScrollableFrame(
            table_container, fg_color="transparent"
        )
        self.table_scrollable.pack(fill="both", expand=True)

        try:

            # Configure scrollable frame for table expansion
            inner = getattr(self.table_scrollable, "scrollable_frame", None)
            if inner:
                inner.columnconfigure(0, weight=1)
            else:
                self.table_scrollable.columnconfigure(0, weight=1)

        except Exception:
            pass

        # Create table header
        self._create_table_header()

    def _create_table_header(self) -> None:
        """Create the header row in the scrollable table, with styled labels."""

        # Clear any existing header widgets first
        for widget in self.table_scrollable.winfo_children():
            info = widget.grid_info()

            if info.get("row") == 0:
                widget.destroy()

        # FRAME FOR THE HEADER
        header_frame = ctk.CTkFrame(
            self.table_scrollable, fg_color=AppStyles.PRIMARY_COLOR, corner_radius=5
        )

        # We place in Grid Row 0, column 0, Sticky Ew to stretch
        header_frame.grid(row=0, column=0, sticky="ew", padx=2, pady=(2, 0))

        # We configure column 0 of the scrollable for the header to stretch:
        try:
            inner = getattr(self.table_scrollable, "scrollable_frame", None)

            if inner:
                inner.columnconfigure(0, weight=1)
            else:
                self.table_scrollable.columnconfigure(0, weight=1)

        except Exception:
            pass

        # Configure columns inside the header_frame
        # Small column ID, Name larger, small price
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=4)
        header_frame.columnconfigure(2, weight=2)

        # ID header
        id_lbl = ctk.CTkLabel(
            header_frame, text="ID", font=AppStyles.NORMAL_FONT, text_color="#ffffff"
        )
        id_lbl.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        # Name header
        name_lbl = ctk.CTkLabel(
            header_frame,
            text="Product Name",
            font=AppStyles.NORMAL_FONT,
            text_color="#ffffff",
        )
        name_lbl.grid(row=0, column=1, sticky="ew", padx=8, pady=8)

        # Price header
        price_lbl = ctk.CTkLabel(
            header_frame, text="Price", font=AppStyles.NORMAL_FONT, text_color="#ffffff"
        )
        price_lbl.grid(row=0, column=2, sticky="ew", padx=8, pady=8)

    def _create_refresh_button(self) -> None:
        """Create refresh button at bottom of inventory tab"""

        button_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=(5, 10))

        refresh_btn = StyledButton(
            button_frame,
            text="Refresh Inventory",
            command=lambda: (self.read_products(), self.update_summary_data()),
            button_type="primary",
            width=150,
        )
        refresh_btn.pack(side="right", padx=15)

    def read_products(self) -> None:
        """Read all products from the database and populate the table."""

        try:
            products: List[Tuple[Any, ...]] = self.db_manager.get_all_products()

            # Remove previous rows: widgets with grid row> = 1
            for widget in self.table_scrollable.winfo_children():
                info = widget.grid_info()
                row = info.get("row")

                if isinstance(row, int) and row >= 1:
                    widget.destroy()

            # Populate new rows
            for idx, p in enumerate(products, start=1):
                prod_id = p[0]
                name = p[1]

                try:
                    price_val = float(p[2])
                except Exception:
                    price_val = 0.0

                price_str = f"${price_val:,.2f}"

                # Alternate background color
                row_bg = "#2b2b2b" if idx % 2 == 1 else "#242424"

                row_frame = ctk.CTkFrame(
                    self.table_scrollable, fg_color=row_bg, corner_radius=0
                )

                row_frame.grid(row=idx, column=0, sticky="ew", padx=2, pady=0)

                # Configure columns: same scheme as header
                row_frame.columnconfigure(0, weight=1)
                row_frame.columnconfigure(1, weight=4)
                row_frame.columnconfigure(2, weight=2)

                # ID label
                id_lbl = ctk.CTkLabel(
                    row_frame, text=str(prod_id), font=AppStyles.NORMAL_FONT, anchor="w"
                )
                id_lbl.grid(row=0, column=0, sticky="ew", padx=8, pady=6)

                # Name label
                name_lbl = ctk.CTkLabel(
                    row_frame, text=name, font=AppStyles.NORMAL_FONT, anchor="w"
                )
                name_lbl.grid(row=0, column=1, sticky="ew", padx=8, pady=6)

                # Price label, aligned to the right
                price_lbl = ctk.CTkLabel(
                    row_frame, text=price_str, font=AppStyles.NORMAL_FONT, anchor="e"
                )
                price_lbl.grid(row=0, column=2, sticky="ew", padx=8, pady=6)

        except Exception as e:
            self.result_label.show_error(f"Error loading products: {e}")

    def update_summary_data(self) -> None:
        """Update the statistics panel with current data."""

        self.stats_panel.update_stats()
