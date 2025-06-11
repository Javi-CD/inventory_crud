# CRUD Operations Documentation

This document outlines the Create, Read, Update, and Delete (CRUD) operations implemented in the Inventory Management System.

## Overview

The Inventory Management System implements standard CRUD operations for managing product inventory. These operations are handled by the `DatabaseManager` class and exposed through the application's user interface.

## Operations

### Create

**Adding a New Product**

```python
def add_product(self, name: str, price: str) -> None:
    """Add a new product to the database.
    
    Args:
        name: Product name
        price: Product price
    """
    query = 'INSERT INTO products VALUES(NULL, ?, ?)'
    self.execute_query(query, (name, price))
```

#### Process Flow:

1. User enters product name and price in the input form
2. User clicks "Save Product" button
3. System validates the input data (non-empty name and price)
4. System inserts the new product into the database
5. UI refreshes to display the updated product list
6. User receives a success confirmation message

### Read

### Retrieving All Products

```python
def get_all_products(self) -> List[Tuple[Any, ...]]:
    """Get all products from the database.
    
    Returns:
        List[Tuple]: List of product tuples
    """
    query = 'SELECT * FROM products ORDER BY name DESC'
    cursor = self.execute_query(query)
    return cursor.fetchall()
```
#### Process Flow:

1. System queries the database for all products
2. Results are displayed in the product list treeview
3. Products are sorted by name in descending order
4. This operation is called automatically when the application starts and after any modification to the data

### Update

### Updating a Product
```python
def update_product(self, new_name: str, new_price: str, old_name: str, old_price: str) -> None:
    """Update product information.
    
    Args:
        new_name: New product name
        new_price: New product price
        old_name: Original product name
        old_price: Original product price
    """
    query = 'UPDATE products SET name = ?, price = ? WHERE name = ? AND price = ?'
    self.execute_query(query, (new_name, new_price, old_name, old_price))
```

### Delete

## Deleting a Product

```python
def delete_product(self, name: str) -> None:
    """Delete a product from the database.
    
    Args:
        name: Name of the product to delete
    """
    query = 'DELETE FROM products WHERE name = ?'
    self.execute_query(query, (name,))
```

#### Process Flow:

1. User selects a product from the list
2. User clicks "Delete Product" button
3. System prompts for confirmation
4. If confirmed, system deletes the product from the database
5. UI refreshes to display the updated product list
6. User receives a success confirmation message

#### Validation Rules
The application implements several validation rules:

1. Product Selection Validation:

    - When trying to delete or edit a product, the system checks if a product is selected
    - If no product is selected, an error message is displayed
 
2. Input Validation:

    - Product name cannot be empty
    - Product price cannot be empty
    - (Future enhancement: price format validation)

##### Error Handling
The system implements basic error handling for CRUD operations:

1. **Database Connection Errors**: Wrapped in try/except blocks
2. **User Input Validation**: Checks for empty fields before executing operations
3. **Confirmation Dialogs**: Used for destructive operations (delete) to prevent accidental data loss
   
##### Future Enhancements
Planned improvements for the CRUD operations:

1. **Batch Operations**: Ability to perform actions on multiple products at once
2. **Search Functionality**: Filter products by name or price range
3. **Advanced Filtering**: Sort products by different criteria
4. **Data Export/Import**: Export product data to CSV or Excel format
