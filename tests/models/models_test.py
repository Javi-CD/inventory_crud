import unittest
from src.models import Product, Employee


class TestProductModel(unittest.TestCase):
    """Test Product model functionality."""

    def test_product_initialization(self):
        """Test product initialization with default and custom values."""

        # Default initialization
        default_product = Product()
        self.assertIsNone(default_product.id)
        self.assertEqual(default_product.name, "")
        self.assertEqual(default_product.price, 0.0)

        # Custom initialization
        custom_product = Product(id=1, name="Test Product", price=99.99)
        self.assertEqual(custom_product.id, 1)
        self.assertEqual(custom_product.name, "Test Product")
        self.assertEqual(custom_product.price, 99.99)

    def test_product_from_db_tuple(self):
        """Test creating a Product from a database tuple."""

        db_tuple = (5, "Database Product", "149.99")
        product = Product.from_db_tuple(db_tuple)

        self.assertEqual(product.id, 5)
        self.assertEqual(product.name, "Database Product")
        self.assertEqual(product.price, 149.99)

        # Test with None
        self.assertIsNone(Product.from_db_tuple(None))

    def test_product_to_dict(self):
        """Test converting a Product to dictionary."""

        product = Product(id=10, name="Dictionary Product", price=50.25)
        product_dict = product.to_dict()

        self.assertEqual(product_dict["id"], 10)
        self.assertEqual(product_dict["name"], "Dictionary Product")
        self.assertEqual(product_dict["price"], 50.25)

    def test_product_str(self):
        """Test string representation of Product."""

        product = Product(id=7, name="String Product", price=75.50)
        product_str = str(product)

        self.assertEqual(product_str, "ID 7 - String Product - $75.50")


class TestEmployeeModel(unittest.TestCase):
    """Test Employee model functionality."""

    def test_employee_initialization(self):
        """Test employee initialization with default and custom values."""
        # Default initialization
        default_employee = Employee()
        self.assertEqual(default_employee.id, "")
        self.assertEqual(default_employee.name, "")
        self.assertEqual(default_employee.role, "")

        # Custom initialization
        custom_employee = Employee(id="E123", name="John Doe", role="Manager")
        self.assertEqual(custom_employee.id, "E123")
        self.assertEqual(custom_employee.name, "John Doe")
        self.assertEqual(custom_employee.role, "Manager")

    def test_employee_to_dict(self):
        """Test converting an Employee to dictionary."""
        employee = Employee(id="E456", name="Jane Smith", role="Admin")
        employee_dict = employee.to_dict()

        self.assertEqual(employee_dict["id"], "E456")
        self.assertEqual(employee_dict["name"], "Jane Smith")
        self.assertEqual(employee_dict["role"], "Admin")

    def test_employee_str(self):
        """Test string representation of Employee."""

        employee = Employee(id="E789", name="Bob Johnson", role="Clerk")
        employee_str = str(employee)

        self.assertEqual(employee_str, "Bob Johnson (Clerk)")


if __name__ == "__main__":
    unittest.main()
