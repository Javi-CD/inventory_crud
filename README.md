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
├──proyect.toml      # Proyect Dependenies
├── LICENSE          # MIT License file
├── README.md        # Project documentation
├── main.py          # Application entry point
├── requirements.txt # Project dependencies
├── assets/          # Assets Files
├── doc/             # Documentation folder
├── tests/           # Test directory
│   ├── core/        # Core functionality tests
│   │   └── database_test.py  # Database operations tests
│   │   └── __init__.py
│   └── ui/          # UI component tests
│   │    └── components_test.py # UI components tests
│   │    └── __init__.py
│   │
│   └── conftest.py
│   └── __init__.py
└── src/
    ├── models/      # Models files
    │   └── models.py # Product model
    │   └── __init__.py  
    │
    ├── core/        # Core business logic
    │   └── database.py  # Database operations
    │   └── __init__.py  
    │
    ├── db/          # Database files
    │   ├── __init__.py
    │   └── inventory.db # SQLite database
    │
    └── ui/          # User interface
        ├── components/  # UI building blocks
        │   └── inventory/
        │   └── product/
        │   └── login.py
        │   └── components.py # Reusable UI components
        │   └── stats_panel.py 
        │   └── __init__.py
        │
        ├── __init__.py
        ├── app.py       # Main application class
        └── styles.py    # UI styling definitions  
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
poetry shell

# Execute program
python main.py
```
## Running Tests

```python
# Run all tests
python -m unittest discover tests

# Run specific test module
python -m tests.core.database_test
python -m tests.ui.components_test
python -m unittest tests.models.models_test
python -m unittest tests.ui.stats_panel_test
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.



