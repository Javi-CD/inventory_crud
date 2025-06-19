from typing import Dict


class Employee:
    """Model representing an employee."""

    def __init__(self, id: str = "", name: str = "", role: str = "") -> None:
        """Initialize an Employee instance.

        Args:
            id (str, optional): The employee ID. Defaults to "".
            name (str, optional): The employee name. Defaults to "".
            role (str, optional): The employee role. Defaults to "".
        """
        self.id = id
        self.name = name
        self.role = role

    def to_dict(self) -> Dict[str, str]:
        """Convert Employee to dictionary.

        Returns:
            Dict[str, str]: A dictionary representation of the employee.
        """

        return {"id": self.id, "name": self.name, "role": self.role}

    def __str__(self) -> str:
        """Convert Employee to string representation.

        Returns:
            str: A string representation of the employee.
        """

        return f"{self.name} ({self.role})"
