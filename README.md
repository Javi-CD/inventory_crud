# Inventory Management System

A simple inventory management system built with Python and Tkinter.

## Features

- Add new products with name and price
- View all products in a sortable list
- Update existing product information
- Delete products from inventory
- Data storage using SQLite database

## Project Structure

```yaml
inventory_crud/
├── LICENSE          # MIT License file
├── README.md        # Project documentation
├── main.py          # Application entry point
├── requirements.txt # Project dependencies
├── doc/             # Documentation folder
└── src/
    ├── models/ Models files
    │   └── products.py # Product model
    │
    ├── core/        # Core business logic
    │   └── database.py  # Database operations
    │
    ├── db/          # Database files
    │   ├── __init__.py
    │   └── inventory.db # SQLite database
    │
    └── ui/          # User interface
        ├── __init__.py
        ├── app.py       # Main application class
        └── frame.py     # UI components
```

## How to Run

```bash

# Clone repository
git clone https://github.com/Javi-CD/inventory_crud.git

# Change to the Work Directory
cd inventory_crud

# Execute program
python main,py
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.


These changes modularize your application by:
1. Moving database operations to a dedicated  class
2. Creating a `Product` data model
3. Separating UI components into reusable classes
4. Improving the organization of the codebase with clear responsibilities for each module