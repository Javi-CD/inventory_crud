from tkinter import messagebox
from src.core.database import DatabaseManager
from src.ui.components.frame import ProductFrame, ProductListFrame, EditProductDialog

class App:
    """Main application class for the Inventory Management System."""
    
    def __init__(self, window) -> None:
        self.root = window
        self.root.title("Inventory Management System")
        self.db_name = 'src/db/inventory.db'
        
        # Initialize database manager
        self.db_manager = DatabaseManager(self.db_name)
        
        # Initialize UI components
        self.product_frame = ProductFrame(self.root, self.add_product)
        self.product_list = ProductListFrame(self.root, self.delete_product, self.show_edit_dialog)
        
        # Load initial data
        self.refresh_product_list()
    
    def refresh_product_list(self) -> None:
        """Refresh the product list display"""
        products = self.db_manager.get_all_products()
        self.product_list.update_product_list(products)
    
    def add_product(self, name: str, price: str) -> None:
        """Add a new product"""
        if not name or not price:
            messagebox.showerror('Error', 'Name and Price are required')
            return
        
        self.db_manager.add_product(name, price)
        messagebox.showinfo('Success', f'Product {name} added successfully')
        self.refresh_product_list()
    
    def delete_product(self, name: str) -> None:
        """Delete the selected product"""
        if messagebox.askyesno('Confirm Deletion', f'Are you sure you want to delete the product "{name}"?'):
            self.db_manager.delete_product(name)
            messagebox.showinfo('Success', f'Product "{name}" deleted successfully')
            self.refresh_product_list()
    
    def show_edit_dialog(self, name: str, price: str) -> None:
        """Show dialog to edit a product"""
        EditProductDialog(self.root, name, price, 
                         lambda new_name, new_price: self.edit_product(new_name, new_price, name, price))
    
    def edit_product(self, new_name: str, new_price: str, old_name: str, old_price: str) -> None:
        """Update a product's details"""
        self.db_manager.update_product(new_name, new_price, old_name, old_price)
        self.refresh_product_list()
        messagebox.showinfo('Success', f'Product {old_name} updated successfully')