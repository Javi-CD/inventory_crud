import customtkinter as ctk
import tkinter as tk
from typing import Any, Callable, Dict, List, Tuple

from src.core.database import DatabaseManager
from src.models.models import Employee
from .components import MessageLabel, StyledButton
from src.ui.styles import AppStyles


class InventoryFrame(ctk.CTkFrame):
    """
    Frame for inventory management: provides two tabs—
    1) Product Management (CRUD)
    2) Inventory View (table + statistics)
    """

    def __init__(
        self,
        master: Any,
        db_manager: DatabaseManager,
        employee: Employee,
        on_logout: Callable[[], None],
    ) -> None:
        """
        Initialize InventoryFrame.

        Args:
            master (Any): Parent widget.
            db_manager (DatabaseManager): Instance of DatabaseManager.
            employee (Employee): Logged-in Employee instance.
            on_logout (Callable[[], None]): Callback to invoke when user logs out.
        """
        super().__init__(master)
        self.db_manager: DatabaseManager = db_manager
        self.employee: Employee = employee
        self.on_logout: Callable[[], None] = on_logout

        # Create widgets: header, message label, tabs, logout button

        self._create_widgets()

        # Initial load of products and statistics

        self.read_products()
        self.update_summary_data()

    def _create_widgets(self) -> None:
        """
        Create header, message label, tabbed interface, and logout button.
        """
        # Header with employee info

        self._create_header()

        # Message label to show feedback (errors/success/info)

        self.result_label: MessageLabel = MessageLabel(self)
        self.result_label.pack(pady=5)

        # Tabbed interface for CRUD and Inventory view

        self._create_tabbed_interface()

        # Logout button

        logout_btn = StyledButton(
            self, text="Logout", command=self.on_logout, button_type="neutral"
        )
        logout_btn.pack(pady=10)

    def _create_header(self) -> None:
        """
        Create header section with title and user info.
        """
        title = ctk.CTkLabel(
            self,
            text=f"Inventory Management - {self.employee.name}",
            font=AppStyles.TITLE_FONT,
        )
        title.pack(pady=15)

        emp_info = ctk.CTkLabel(
            self,
            text=f"User ID: {self.employee.id} | Role: {self.employee.role}",
            font=AppStyles.NORMAL_FONT,
        )
        emp_info.pack(pady=(0, 10))

    def _create_tabbed_interface(self) -> None:
        """
        Set up CTkTabview with two tabs: 'Product Management' and 'Inventory'.
        """
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Optional subtitle

        main_title = ctk.CTkLabel(
            main_frame, text="Inventory System", font=AppStyles.HEADER_FONT
        )
        main_title.pack(padx=15, pady=(0, 5))

        # Create the tab view

        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)

        # Add two tabs

        self.tabview.add("Product Management")
        self.tabview.add("Inventory")

        # Build each tab's contents

        self._create_product_management_tab(self.tabview.tab("Product Management"))
        self._create_inventory_tab(self.tabview.tab("Inventory"))

    def _create_product_management_tab(self, parent_tab: Any) -> None:
        """
        Configure the 'Product Management' tab: form and CRUD action buttons.
        :param parent_tab: the CTkFrame for this tab
        """
        self._create_form(parent_tab)
        self._create_action_buttons(parent_tab)

    def _create_inventory_tab(self, parent_tab: Any) -> None:
        """
        Configure the 'Inventory' tab: show product table (scrollable CTk-based table) and statistics.
        Now expanded to fill available space, with proper padding between columns.
        :param parent_tab: the CTkFrame for this tab
        """
        # Contrainer Frame for the table: expand in all width

        table_container = ctk.CTkFrame(parent_tab)
        # Now we let it expand vertically and horizontally

        table_container.pack(padx=10, pady=10, fill="both", expand=True)

        # Scrollable frame for ranks: occupies the entire remaining space in Table_Container
        # We use grid instead of internal pack to configure pesos

        self.table_scrollable: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(
            table_container, fg_color="transparent"
        )
        # We pack with Fill and Expand to use the entire space

        self.table_scrollable.pack(fill="both", expand=True)

        # Configure colonconfigure inside the scrollable:
        # assuming that ctkscrollableframe places its widgets in an internal frame with Grid,
        # We can force column 0 to stretch:

        try:
            # If ctkscrollableframe exposes a scrollable_frame attribute, use it:

            inner = getattr(self.table_scrollable, "scrollable_frame", None)
            if inner:
                inner.columnconfigure(0, weight=1)
            else:
                # Fallback: Set your own

                self.table_scrollable.columnconfigure(0, weight=1)
        except Exception:
            pass

        # Create Header of the table

        self._create_table_header()

        # Frame for summary section (Statistics) under the table

        summary_frame = ctk.CTkFrame(parent_tab)
        summary_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Section title

        summary_title = ctk.CTkLabel(
            summary_frame, text="Inventory Summary", font=AppStyles.HEADER_FONT
        )
        summary_title.pack(pady=(5, 10))

        # Container Dividend statistics into two columns

        main_container = ctk.CTkFrame(summary_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)

        # LEFT COLUMN: KEY STATISTICS (as before) ...

        stats_frame = ctk.CTkFrame(main_container)
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

        self.total_products_label: ctk.CTkLabel = ctk.CTkLabel(
            stats_grid, text="Loading...", font=AppStyles.NORMAL_FONT
        )
        self.total_products_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        self.total_value_label: ctk.CTkLabel = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.total_value_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        self.avg_price_label: ctk.CTkLabel = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.avg_price_label.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        self.max_price_label: ctk.CTkLabel = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.max_price_label.grid(row=3, column=1, sticky="w", padx=5, pady=2)
        self.min_price_label: ctk.CTkLabel = ctk.CTkLabel(
            stats_grid, text="", font=AppStyles.NORMAL_FONT
        )
        self.min_price_label.grid(row=4, column=1, sticky="w", padx=5, pady=2)

        # Right column: categories

        categories_container = ctk.CTkFrame(main_container)
        categories_container.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        categories_title = ctk.CTkLabel(
            categories_container, text="Product Categories", font=AppStyles.NORMAL_FONT
        )
        categories_title.pack(anchor="w", padx=10, pady=(5, 5))

        categories_scroll = ctk.CTkScrollableFrame(
            categories_container, width=200, height=150
        )
        categories_scroll.pack(fill="both", expand=True, padx=10, pady=5)
        self.categories_frame: ctk.CTkScrollableFrame = categories_scroll

        # Refresh button
        button_frame = ctk.CTkFrame(summary_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(5, 10))

        refresh_btn = StyledButton(
            button_frame,
            text="Refresh Inventory",
            command=lambda: (self.read_products(), self.update_summary_data()),
            button_type="primary",
            width=150,
        )
        refresh_btn.pack(side="right", padx=15)

    def _create_table_header(self) -> None:
        """
        Create the header row in the scrollable table, with styled labels.
        Now with proper column weights and padding so se expanda horizontalmente.
        """
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

    def _create_form(self, parent: Any = None) -> None:
        """
        Create form entries for creating/updating/deleting a product.
        :param parent: parent widget (tab frame). If None, uses self.
        """
        container = parent if parent else self
        form_frame = ctk.CTkFrame(container)
        form_frame.pack(pady=10, padx=20, fill="x")

        # ID field (for update/delete)

        id_label = ctk.CTkLabel(form_frame, text="Product ID (for update/delete)")
        id_label.pack(padx=20, pady=(10, 0), anchor="w")
        self.id_entry: ctk.CTkEntry = ctk.CTkEntry(
            form_frame, placeholder_text="Product ID"
        )
        self.id_entry.pack(padx=20, pady=(0, 10), fill="x")

        # Name field

        name_label = ctk.CTkLabel(form_frame, text="Product Name")
        name_label.pack(padx=20, pady=(5, 0), anchor="w")
        self.name_entry: ctk.CTkEntry = ctk.CTkEntry(
            form_frame, placeholder_text="Name"
        )
        self.name_entry.pack(padx=20, pady=(0, 10), fill="x")

        # Price field

        price_label = ctk.CTkLabel(form_frame, text="Price")
        price_label.pack(padx=20, pady=(5, 0), anchor="w")
        self.price_entry: ctk.CTkEntry = ctk.CTkEntry(
            form_frame, placeholder_text="Price"
        )
        self.price_entry.pack(padx=20, pady=(0, 10), fill="x")

    def _create_action_buttons(self, parent: Any = None) -> None:
        """
        Create CRUD action buttons: Create, Refresh List, Update, Delete.
        :param parent: parent widget (tab frame). If None, uses self.
        """
        container = parent if parent else self
        button_frame = ctk.CTkFrame(container)
        button_frame.pack(pady=15)

        # Create button

        create_btn = StyledButton(
            button_frame,
            text="Create",
            command=self.create_product,
            width=130,
            button_type="success",
        )
        create_btn.grid(row=0, column=0, padx=10, pady=5)

        # Refresh list button

        read_btn = StyledButton(
            button_frame,
            text="Refresh List",
            command=lambda: (
                self.read_products(),
                self.result_label.show_info("List refreshed."),
            ),
            width=130,
            button_type="primary",
        )
        read_btn.grid(row=0, column=1, padx=10, pady=5)

        # Update button

        update_btn = StyledButton(
            button_frame,
            text="Update",
            command=self.update_product,
            width=130,
            button_type="warning",
        )
        update_btn.grid(row=1, column=0, padx=10, pady=5)

        # Delete button

        delete_btn = StyledButton(
            button_frame,
            text="Delete",
            command=self.delete_product,
            width=130,
            button_type="danger",
        )
        delete_btn.grid(row=1, column=1, padx=10, pady=5)

    def create_product(self) -> None:
        """
        Create a new product in the database, then switch to Inventory tab and refresh.
        """
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name or not price:
            self.result_label.show_error("Please complete all fields.")
            return

        try:
            price_val = float(price)
        except ValueError:
            self.result_label.show_error("Price must be numeric.")
            return

        try:
            self.db_manager.add_product(name, str(price_val))
            self.clear_fields()
            # Switch to Inventory tab and refresh

            self.tabview.set("Inventory")
            self.read_products()
            self.update_summary_data()
            self.result_label.show_success(f"Product '{name}' added successfully.")
        except Exception as e:
            self.result_label.show_error(f"Error when adding product: {e}")

    def read_products(self) -> None:
        """
        Read all products from the database and populate the custom table in Inventory tab.
        Clears existing rows (except header) and inserts up-to-date data.
        """
        try:
            products: List[Tuple[Any, ...]] = self.db_manager.get_all_products()
            # Eliminar filas previas: widgets con grid row >= 1
            for widget in self.table_scrollable.winfo_children():
                info = widget.grid_info()
                row = info.get("row")
                if isinstance(row, int) and row >= 1:
                    widget.destroy()

            # Poblar nuevas filas
            for idx, p in enumerate(products, start=1):
                prod_id = p[0]
                name = p[1]
                try:
                    price_val = float(p[2])
                except Exception:
                    price_val = 0.0
                price_str = f"${price_val:,.2f}"

                # Alternar color de fondo
                row_bg = "#2b2b2b" if idx % 2 == 1 else "#242424"

                row_frame = ctk.CTkFrame(
                    self.table_scrollable, fg_color=row_bg, corner_radius=0
                )
                # grid en row idx, column 0, sticky ew para expandir
                row_frame.grid(row=idx, column=0, sticky="ew", padx=2, pady=0)

                # Configurar columnas: mismo esquema que header
                # Aseguramos que la columna 0 del scrollable tenga weight=1,
                # y que cada row_frame expanda sus celdas:
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
                # Price label, alineado a la derecha
                price_lbl = ctk.CTkLabel(
                    row_frame, text=price_str, font=AppStyles.NORMAL_FONT, anchor="e"
                )
                price_lbl.grid(row=0, column=2, sticky="ew", padx=8, pady=6)

        except Exception as e:
            self.result_label.show_error(f"Error loading products: {e}")

    def update_product(self) -> None:
        """
        Update an existing product based on ID, then switch to Inventory tab and refresh.
        """
        id_text = self.id_entry.get().strip()
        try:
            product_id = int(id_text)
        except ValueError:
            self.result_label.show_error("Invalid ID. Must be a number.")
            return

        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()
        if not name or not price:
            self.result_label.show_error("Please complete all fields.")
            return

        try:
            price_val = float(price)
        except ValueError:
            self.result_label.show_error("Price must be numeric.")
            return

        existing = self.db_manager.get_product_by_id(product_id)
        if not existing:
            self.result_label.show_error(f"No product found with ID {product_id}.")
            return

        try:
            self.db_manager.update_product(product_id, name, str(price_val))
            self.clear_fields()
            self.tabview.set("Inventory")
            self.read_products()
            self.update_summary_data()
            self.result_label.show_success(
                f"Product ID {product_id} updated successfully."
            )
        except Exception as e:
            self.result_label.show_error(f"Error when updating product: {e}")

    def delete_product(self) -> None:
        """
        Delete a product by ID, then switch to Inventory tab and refresh.
        """
        id_text = self.id_entry.get().strip()
        try:
            product_id = int(id_text)
        except ValueError:
            self.result_label.show_error("Invalid ID. Must be a number.")
            return

        existing = self.db_manager.get_product_by_id(product_id)
        if not existing:
            self.result_label.show_error(f"No product found with ID {product_id}.")
            return

        try:
            self.db_manager.delete_product(product_id)
            self.clear_fields()
            self.tabview.set("Inventory")
            self.read_products()
            self.update_summary_data()
            self.result_label.show_success(
                f"Product ID {product_id} deleted successfully."
            )
        except Exception as e:
            self.result_label.show_error(f"Error when deleting product: {e}")

    def clear_fields(self) -> None:
        """
        Clear the form entry fields.
        """
        try:
            self.id_entry.delete(0, "end")
            self.name_entry.delete(0, "end")
            self.price_entry.delete(0, "end")
        except Exception:
            pass

    def update_summary_data(self) -> None:
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

    def _on_table_row_click(self, event: tk.Event) -> None:
        """
        Optional: if you want to bind clicks on rows to fill the form.
        Currently, rows are CTkFrames, so binding requires more work.
        """
        pass  # not implemented; for CTk-based rows, you could bind events on each label/frame
