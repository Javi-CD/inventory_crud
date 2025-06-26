# ✨ Inventory Management System ✨

A inventory management system built with Python and CustomTkinter.

![image](https://github.com/user-attachments/assets/1805c98f-6341-4fa8-a4c5-cf35b7e1ee56)

## Features ⭐

- Add new products with name and price
- View all products in a sortable list
- Update existing product information
- Delete products from inventory
- Data storage using SQLite database
- Automatic code documentation

## Project Structure 📂

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
        │   └── login/
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
poetry install

# Activate the virtual environment (optional)
poetry shell

# Execute program
python main.py
```
## Building Executable ⚙️

To create a standalone executable version of the application:
````bash
# Make sure PyInstaller is installed
pip install pyinstaller

# Change to the directory that stores the binaries
cd build

# Run the build script or double click in the file
.\scripts\build_app.bat
````
>[!NOTE]
The executable will be generated in the ``build`` directory as ``InventoryManager.exe``. This standalone version can be distributed to users who don't have Python installed.

## Running Tests 📋

```python
# Run all tests
python -m unittest discover tests

# Run specific test module
python -m tests.core.database_test
python -m tests.ui.components_test
python -m unittest tests.models.models_test
python -m unittest tests.ui.stats_panel_test
```
## DOC 📖
⇨ [Documentation in Read the Docs](https://inventory-crud.readthedocs.io/en/latest/)

## License ©️
This project is licensed under the ``MIT License`` - see the [LICENCE](./LICENCE) file for details.
