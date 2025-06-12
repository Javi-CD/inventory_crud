import customtkinter as ctk
import os
from typing import List, Dict, Any, Optional
from src.core.database import DatabaseManager

class InventoryApp:
    """Main application class for the Inventory Management System."""
    
    def __init__(self) -> None:
        # Visual configuration
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Initialize the database
        self.db_path = os.path.join('src', 'db', 'inventory.db')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.db_manager = DatabaseManager(self.db_path)
        
        # Create the main window
        self.app = ctk.CTk()
        self.app.title("Sistema de Inventario")
        self.app.geometry("600x620")
        self.app.resizable(False, False)
        
        # Set the login frame
        self.setup_login_frame()
        
    def setup_login_frame(self) -> None:
        """Configurar el frame de login."""
        self.login_frame = ctk.CTkFrame(self.app)
        self.login_frame.pack(padx=40, pady=40, fill="both", expand=True)

        login_title = ctk.CTkLabel(self.login_frame, text="Acceso de Empleado", font=ctk.CTkFont(size=24, weight="bold"))
        login_title.pack(pady=20)

        self.emp_id_entry = ctk.CTkEntry(self.login_frame, placeholder_text="ID del empleado")
        self.emp_id_entry.pack(pady=10, padx=20, fill="x")

        self.emp_name_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Nombre del empleado")
        self.emp_name_entry.pack(pady=10, padx=20, fill="x")

        self.emp_role_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Cargo o rol")
        self.emp_role_entry.pack(pady=10, padx=20, fill="x")

        login_btn = ctk.CTkButton(self.login_frame, text="Ingresar", command=self.open_crud)
        login_btn.pack(pady=20)

        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="gray")
        self.error_label.pack()
    
    def open_crud(self) -> None:
        """Validate login and open the CRUD interface."""
        if not self.emp_id_entry.get().strip() or not self.emp_name_entry.get().strip() or not self.emp_role_entry.get().strip():
            self.error_label.configure(text="Por favor completa todos los campos.")
            return

        # Save employee information
        self.employee = {
            'id': self.emp_id_entry.get().strip(),
            'name': self.emp_name_entry.get().strip(),
            'role': self.emp_role_entry.get().strip()
        }
        
        # Close login window
        self.login_frame.pack_forget()
        self.create_crud_interface()

    def return_to_login(self) -> None:
        """Return to the login screen."""

        # Hide crude interface
        for widget in self.app.winfo_children():
            widget.pack_forget()
        
        # Show login again
        self.login_frame.pack(padx=40, pady=40, fill="both", expand=True)

    def create_crud_interface(self) -> None:
        """Create the CRUD interface for managing products."""
        # Title
        title = ctk.CTkLabel(self.app, text=f"Gestión de Inventario - {self.employee['name']}", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=15)

        # Frame for the form
        form_frame = ctk.CTkFrame(self.app)
        form_frame.pack(pady=10, padx=20, fill="x")

        # Text entrances

        self.id_entry = ctk.CTkEntry(form_frame, placeholder_text="ID (para actualizar/eliminar)")
        self.id_entry.pack(padx=20, pady=(10, 5), fill="x")

        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="Nombre del producto")
        self.name_entry.pack(padx=20, pady=5, fill="x")

        self.price_entry = ctk.CTkEntry(form_frame, placeholder_text="Precio")
        self.price_entry.pack(padx=20, pady=(5, 10), fill="x")

        # Buttons
        button_frame = ctk.CTkFrame(self.app)
        button_frame.pack(pady=15)

        # Back button
        volver_btn = ctk.CTkButton(self.app, text="Cerrar Sesión", command=self.return_to_login, fg_color="gray25", hover_color="gray40")
        volver_btn.pack(pady=10)

        # CRUD buttons
        create_btn = ctk.CTkButton(button_frame, text="Crear", command=self.create_product, width=130)
        create_btn.grid(row=0, column=0, padx=10, pady=10)

        read_btn = ctk.CTkButton(button_frame, text="Actualizar Lista", command=self.read_products, width=130)
        read_btn.grid(row=0, column=1, padx=10, pady=10)

        update_btn = ctk.CTkButton(button_frame, text="Actualizar", command=self.update_product, width=130)
        update_btn.grid(row=1, column=0, padx=10, pady=10)

        delete_btn = ctk.CTkButton(button_frame, text="Eliminar", command=self.delete_product, width=130)
        delete_btn.grid(row=1, column=1, padx=10, pady=10)

        # Result label
        self.result_label = ctk.CTkLabel(self.app, text="", text_color="gray")
        self.result_label.pack(pady=5)

        # FRAME FOR THE LIST OF PRODUCTS
        list_frame = ctk.CTkFrame(self.app)
        list_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.product_listbox = ctk.CTkTextbox(list_frame, height=200, state="disabled")
        self.product_listbox.pack(padx=15, pady=15, fill="both", expand=True)
        
        # Load products
        self.read_products()
    
    def create_product(self) -> None:
        """Create a new product in the database."""
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name or not price:
            self.result_label.configure(text="Completa todos los campos.")
            return

        try:
            price = float(price)
        except ValueError:
            self.result_label.configure(text="El precio debe ser numérico.")
            return

        try:
            self.db_manager.add_product(name, str(price))
            self.clear_fields()
            self.read_products()
            self.result_label.configure(text=f"Producto '{name}' agregado correctamente.")
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")

    def read_products(self) -> None:
        """Read and display all products in the listbox."""
        try:
            products = self.db_manager.get_all_products()
            
            self.product_listbox.configure(state="normal")
            self.product_listbox.delete("0.0", "end")
            
            if not products:
                self.product_listbox.insert("end", "No hay productos en la base de datos.\n")
            else:
                for p in products:
                    self.product_listbox.insert("end", f"ID {p[0]} - {p[1]} - ${float(p[2]):.2f}\n")
            
            self.product_listbox.configure(state="disabled")
            self.result_label.configure(text="Lista de productos actualizada.")
        except Exception as e:
            self.result_label.configure(text=f"Error al cargar productos: {str(e)}")

    def update_product(self) -> None:
        """Update an existing product."""
        try:
            product_id = int(self.id_entry.get())
        except ValueError:
            self.result_label.configure(text="ID inválido. Debe ser un número.")
            return

        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name or not price:
            self.result_label.configure(text="Completa todos los campos.")
            return

        try:
            price = float(price)
        except ValueError:
            self.result_label.configure(text="El precio debe ser numérico.")
            return

        product = self.db_manager.get_product_by_id(product_id)
        if not product:
            self.result_label.configure(text=f"No existe un producto con ID {product_id}.")
            return

        try:
            self.db_manager.update_product(product_id, name, str(price))
            self.clear_fields()
            self.read_products()
            self.result_label.configure(text=f"Producto ID {product_id} actualizado correctamente.")
        except Exception as e:
            self.result_label.configure(text=f"Error al actualizar: {str(e)}")

    def delete_product(self) -> None:
        """Delete an existing product."""
        try:
            product_id = int(self.id_entry.get())
        except ValueError:
            self.result_label.configure(text="ID inválido. Debe ser un número.")
            return

        product = self.db_manager.get_product_by_id(product_id)
        if not product:
            self.result_label.configure(text=f"No existe un producto con ID {product_id}.")
            return

        try:
            self.db_manager.delete_product(product_id)
            self.clear_fields()
            self.read_products()
            self.result_label.configure(text=f"Producto ID {product_id} eliminado correctamente.")
        except Exception as e:
            self.result_label.configure(text=f"Error al eliminar: {str(e)}")

    def clear_fields(self) -> None:
        """Clear input fields."""
        self.id_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.price_entry.delete(0, "end")

    def run(self) -> None:
        """Start the application."""
        self.app.mainloop()