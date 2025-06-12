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
    ├── models/     # Models files
    │   └── products.py # Product model
    │
    ├── core/        # Core business logic
    │   └── database.py  # Database operations
    │
    ├── db/          # Database files
    │   ├── __init__.py
    │   └── inventory.db # SQLite database
    │
    └── ui/
    
        │     # User interface
        ├─      
        ├── __init__.py
        ├── app.py       # Main application class
        └── styles.py    
```

## How to Run

```bash

# Clone repository
git clone https://github.com/Javi-CD/inventory_crud.git

# Change to the Work Directory
cd inventory_crud

# if you don't have poetry installed
pip install poetry 

# Install dependecies 
pip install poetry

# Activate the virtual environment
pip install poetry

# Execute program
python main,py
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.



