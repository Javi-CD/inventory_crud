# ✨ Inventory Management System ✨

A inventory management system built with Python and CustomTkinter.

![image](https://github.com/user-attachments/assets/1805c98f-6341-4fa8-a4c5-cf35b7e1ee56)

---

## Features ⭐

- Add new products with name and price
- View all products in a sortable list
- Update existing product information
- Delete products from inventory
- Data storage using SQLite database
- Automatic code documentation

---

## Project Structure 📂

```yaml
inventory_crud/
├── proyect.toml         # Proyect dependenies
├── requirements.txt     # Proyect dependencies
├── LICENSE              # MIT License file
├── README.md            # Project documentation
├── CODE_OF_CONDUCT.md   # Code of Conduct File
├── CONTRIBUTING.md      # Explanatory file for contributions
├── main.py              # Application entry point
│     
├── assets/              # Assets Files
├── docs/                # Documentation folder
├── tests/               # Unit Test Directory
│   ├── core/            # Core functionality tests
│   ├── ui/              # UI component tests
│   ├── models/          # Models functionality tests
│   ├── intregation/     # Integrations functionality tests
│   │
│   ├── conftest.py
│   └── __init__.py
│
└── src/
    ├── models/          # Models files
    │   ├── employee_model.py
    │   ├── product_model.py
    │   └── __init__.py  
    │
    ├── core/            # Core business logic
    │   ├── database.py  # Database operations
    │   └── __init__.py  
    │
    ├── db/              # Database files
    │   ├── __init__.py
    │   └── inventory.db # SQLite database
    │
    ├── ui/              # User interface
    │   ├── components/  # UI building blocks
    │   │   ├── inventory/
    │   │   ├── product/
    │   │   ├── login/
    │   │   ├── stats_panel/
    │   │   │
    │   │   ├── components.py 
    │   │   └── __init__.py
    │   │
    │   ├── __init__.py
    │   ├── app.py       # Main application class
    │   └── styles.py    # UI styling definitions  
    │
    ├── utils/           # Utilities Directory
    │    ├── passwor_utils.py
    │    ├── placeholders_illustration.py
    │    └── __init__.py
    │
    └── __init__.py

```

---

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

---

## Building Executable ⚙️

To create a standalone executable version of the application:
````bash
# Make sure PyInstaller is installed
pip install pyinstaller

# Or install PyInstaller with Pip
pip install pyinstaller

# Change to the directory that stores the binaries
cd .\build

# Run the build script or double click in the file
.\scripts\build_app.bat
````
>[!NOTE]
The executable will be generated in the ``build`` directory as ``InventoryManager.exe``. This standalone version can be distributed to users who don't have Python installed.

---

## Running Tests 📋

```python
# Run all tests
python -m unittest discover tests

# Run specific test module
python -m tests.core.database_test
python -m tests.ui.components_test
...
```
---

## DOC 📖
→ [Documentation](https://inventory-crud.readthedocs.io/en/latest/)

### Generating Documentation 

To build the HTML documentation locally using Sphinx, you can use the provided batch script `build_docs.bat`

```bash

# Install Sphinx if you don't have it with Poetry
poetry add --dev sphinx sphinx-autobuild sphinx-rtd-theme

# Or install Sphinx with Pip
pip install sphinx sphinx-autobuild sphinx-rtd-theme

# Change to the directory containing the scripts
cd .\scripts

# Run the script or double-click the file
.\build_docs.bat

```


>[!NOTE]
>You can view the documentation locally by opening the `index.html` file in your browser located in the `./docs/build/html/index.html` directory or deploying it in your preferred service (e.g., *Read The Doc*).

---

## License ©️
This project is licensed under the ``MIT License`` - see the [LICENCE](./LICENCE) file for details.
