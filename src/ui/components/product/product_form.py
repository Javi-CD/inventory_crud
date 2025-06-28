from typing import Any, Callable

import customtkinter as ctk

from src.core.database import DatabaseManager

from .. import MessageLabel, StyledButton


class ProductManagementTab:
    """
    Tab for product management (create, update, delete operations)
    """

    def __init__(
        self,
        parent: Any,
        db_manager: DatabaseManager,
        result_label: MessageLabel,
        refresh_callback: Callable[[], None],
        switch_to_inventory_tab,
    ) -> None:
        self.parent = parent
        self.db_manager = db_manager
        self.result_label = result_label
        self.refresh_callback = refresh_callback

        # Callback to change to the inventory tab
        self.switch_to_inventory_tab = switch_to_inventory_tab

        self._create_form()
        self._create_action_buttons()

    def _create_form(self) -> None:
        """Create form entries for creating/updating/deleting a product."""
        form_frame = ctk.CTkFrame(self.parent)
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

    def _create_action_buttons(self) -> None:
        """
        Create CRUD action buttons: Create, Refresh List, Update, Delete.
        """
        button_frame = ctk.CTkFrame(self.parent)
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
                self.refresh_callback(),
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
        Create a new product in the database, then refresh.
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

            # Refresh data
            self.refresh_callback()
            self.switch_to_inventory_tab()  # Change to inventory tab

            self.result_label.show_success(f"Product '{name}' added successfully.")

        except Exception as e:
            self.result_label.show_error(f"Error when adding product: {e}")

    def update_product(self) -> None:
        """
        Update an existing product based on ID, then refresh.
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
            self.refresh_callback()
            self.switch_to_inventory_tab()
            self.result_label.show_success(
                f"Product ID {product_id} updated successfully."
            )

        except Exception as e:
            self.result_label.show_error(f"Error when updating product: {e}")

    def delete_product(self) -> None:
        """
        Delete a product by ID, then refresh.
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
            self.refresh_callback()
            self.switch_to_inventory_tab()
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
