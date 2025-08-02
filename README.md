<div align="center" style="background:rgb(250, 250, 250); border-radius: 10px; padding: 18px 10px 18px 10px; margin-bottom: 18px; box-shadow: 0 1px 6px #e5e7eb;">
  <h1 style="color:#22223b; margin-bottom: 8px; font-weight: 700; letter-spacing: 0.5px;">Inventory Management System</h1>
  <p style="font-size: 1.04em; color: #444; max-width: 600px; margin: 0 auto;">
    A robust, user-friendly inventory management application built with <b>Python</b>, <b>CustomTkinter</b> for a clean UI, <b>SQLite</b> for reliable data storage, and <b>Sphinx</b> for automatic code documentation.<br>
    <span style="color:#6c757d;"><i>Manage your products efficiently, with style and simplicity.</i></span>
  </p>
</div>

<!-- ![image](https://github.com/user-attachments/assets/1805c98f-6341-4fa8-a4c5-cf35b7e1ee56) -->
<p>
  <img src="https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/CUSTOMTKINTER-1a1a1a?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLITE-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/POETRY-181C24?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/SPHINX-222222?style=for-the-badge&logo=sphinx&logoColor=white"/>
  <img src="https://img.shields.io/badge/READ%20THE%20DOCS-8CA1AF?style=for-the-badge&logo=readthedocs&logoColor=white"/>
  <img src="https://img.shields.io/badge/GIT-F05032?style=for-the-badge&logo=git&logoColor=white"/>
</p>

<div align="center">
    <img src="https://img.shields.io/github/license/Javi-CD/inventory_crud?style=for-the-badge"/>
</div>

---

## Features

- Add new products with name and price
- View all products in a sortable list
- Update existing product information
- Delete products from inventory
- Data storage using SQLite database
- Automatic code documentation

---

## Project Structure

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

## Building Executable

To create a standalone executable version of the application:

```bash
# Make sure PyInstaller is installed
poetry add pyinstaller --dev

# Or install PyInstaller with Pip
pip install pyinstaller

# Change to the directory that stores the binaries
cd .\build

# Run the build script or double click in the file
.\scripts\build_app.bat
```

> [!NOTE]
> The executable will be generated in the `build` directory as `InventoryManager.exe`. This standalone version can be distributed to users who don't have Python installed.

---

## Running Tests

```python
# Run all tests
pytest

# Run specific test module
pytest .\tests\core\test_database.py
pytest .\tests\integration\test_app_integration.py
...
```

---

## Documentation

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

> [!NOTE]
> You can view the documentation locally by opening the `index.html` file in your browser located in the `.\docs\build\html\index.html` directory or deploying it in your preferred service (e.g., _Read The Doc_).

---

## CI/CD Integration

This project uses GitHub Actions for Continuous Integration (CI) and Continuous Delivery (CD). Every time you push code or open a pull request, the following checks are run automatically:

- Code formatting with black
- Import sorting with isort
- Linting with flake8

You can view the status of these checks in the GitHub Actions tab of the repository. This ensures code quality and helps prevent errors before merging changes.

---

## License

This project is licensed under the `MIT License` - see the [LICENCE](./LICENCE) file for details.

---

<p align="center" style="margin-top: 30px;">
  <img src="https://img.shields.io/badge/Made%20with%20%E2%9D%A4%EF%B8%8F%20by%20Javi--CD-444444?style=for-the-badge"/>
  <br/>
  <span style="color:#888;font-size:14px;">© 2025 Javi-CD &middot; Inventory Management System &middot; MIT License</span>
</p>
