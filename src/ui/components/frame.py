from tkinter import ttk, Label, Entry, LabelFrame, StringVar, Toplevel
from typing import Callable

class ProductFrame:
    """Frame for product input form"""
    
    def __init__(self, parent, on_save_callback: Callable):
        self.parent = parent
        self.on_save = on_save_callback
        
        # Frame Container
        self.frame = LabelFrame(parent, text='Inventory Management System')
        self.frame.grid(row=0, column=0, columnspan=3, pady=20)
        
        # Name input
        Label(self.frame, text='Name: ').grid(row=1, column=0)
        self.name = Entry(self.frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Price input
        Label(self.frame, text='Price: ').grid(row=2, column=0)
        self.price = Entry(self.frame)
        self.price.grid(row=2, column=1)
        
        # Button Add Product
        ttk.Button(parent, text='Save Product', command=self._on_save_clicked).grid(row=3, columnspan=2, sticky='we')
    
    def _on_save_clicked(self):
        if self.name.get() and self.price.get():
            self.on_save(self.name.get(), self.price.get())
            self.clear_inputs()
    
    def clear_inputs(self):
        self.name.delete(0, 'end')
        self.price.delete(0, 'end')
        self.name.focus()

class ProductListFrame:
    """Frame for displaying the product list"""
    
    def __init__(self, parent, on_delete: Callable, on_edit: Callable):
        self.parent = parent
        self.on_delete = on_delete
        self.on_edit = on_edit
        
        # Table
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Name', anchor='center')
        self.tree.heading('#1', text='Price', anchor='center')
        
        # Button Delete Product
        ttk.Button(parent, text='Delete Product', 
                  command=self._on_delete_clicked).grid(row=5, column=0, sticky='we')

        # Button Edit Product
        ttk.Button(parent, text='Edit Product', 
                  command=self._on_edit_clicked).grid(row=5, column=1, sticky='we')
    
    def _on_delete_clicked(self):
        if self.tree.selection():
            name = self.tree.item(self.tree.selection())['text']
            self.on_delete(name)
    
    def _on_edit_clicked(self):
        if self.tree.selection():
            item = self.tree.selection()[0]
            name = self.tree.item(item)['text']
            price = self.tree.item(item)['values'][0]
            self.on_edit(name, price)
    
    def update_product_list(self, products):
        """Update the product list in the treeview
        
        Args:
            products: List of product tuples (id, name, price)
        """
        # Clear existing items
        for element in self.tree.get_children():
            self.tree.delete(element)
        
        # Add updated products
        for product in products:
            self.tree.insert('', 0, text=product[1], values=product[2])

class EditProductDialog:
    """Dialog for editing a product"""
    
    def __init__(self, parent, old_name, old_price, on_save):
        self.window = Toplevel(parent)
        self.window.title('Edit Product')
        self.window.geometry('255x200')
        self.on_save = on_save

        # Old Name
        Label(self.window, text='Old Name: ').grid(row=0, column=1)
        Entry(self.window, textvariable=StringVar(self.window, value=old_name), 
             state='readonly').grid(row=0, column=2)

        # New Name
        Label(self.window, text='New Name: ').grid(row=1, column=1)
        self.new_name = Entry(self.window)
        self.new_name.grid(row=1, column=2)
        self.new_name.insert(0, old_name)
        
        # Old Price
        Label(self.window, text='Old Price: ').grid(row=2, column=1)
        Entry(self.window, textvariable=StringVar(self.window, value=old_price), 
             state='readonly').grid(row=2, column=2)
        
        # New Price
        Label(self.window, text='New Price: ').grid(row=3, column=1)
        self.new_price = Entry(self.window)
        self.new_price.grid(row=3, column=2)
        self.new_price.insert(0, old_price)
        
        # Button to Save Changes
        ttk.Button(self.window, text='Save Changes', 
                  command=self._save_changes).grid(row=4, column=2, sticky='we')
    
    def _save_changes(self):
        self.on_save(self.new_name.get(), self.new_price.get())
        self.window.destroy()