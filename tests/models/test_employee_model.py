import pytest

from src.models.employee_model import Employee


def test_employee_initialization() -> None:
    """Test employee initialization with default and custom values.

    Returns:
        None
    """
    # Default initialization
    default_employee = Employee()
    assert default_employee.id == ""
    assert default_employee.name == ""
    assert default_employee.role == ""

    # Custom initialization
    custom_employee = Employee(id="E123", name="Javier Perez", role="Manager")
    assert custom_employee.id == "E123"
    assert custom_employee.name == "Javier Perez"
    assert custom_employee.role == "Manager"


def test_employee_to_dict() -> None:
    """Test converting an Employee to dictionary.

    Returns:
        None
    """
    employee = Employee(id="E456", name="Jane Smith", role="Admin")
    employee_dict = employee.to_dict()
    assert employee_dict["id"] == "E456"
    assert employee_dict["name"] == "Jane Smith"
    assert employee_dict["role"] == "Admin"


def test_employee_str() -> None:
    """Test string representation of Employee.

    Returns:
        None
    """
    employee = Employee(id="E789", name="Bob Johnson", role="Clerk")
    employee_str = str(employee)
    assert employee_str == "Bob Johnson (Clerk)"


@pytest.mark.parametrize(
    "employee_id,name,role,expected",
    [
        ("E001", "Alice", "Admin", "Alice (Admin)"),
        ("E002", "Bob", "Manager", "Bob (Manager)"),
        ("E003", "Charlie", "Clerk", "Charlie (Clerk)"),
    ],
)
def test_employee_str_parametrized(
    employee_id: str, name: str, role: str, expected: str
) -> None:
    """Test string representation of Employee with different parameters.

    Args:
        employee_id (str): The ID of the employee.
        name (str): The name of the employee.
        role (str): The role of the employee.
        expected (str): The expected string representation.
    """
    employee = Employee(id=employee_id, name=name, role=role)
    assert str(employee) == expected
