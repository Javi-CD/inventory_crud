import customtkinter as ctk
from typing import Callable, Optional
from src.models.models import Employee
from .components import MessageLabel, StyledButton, FormField
from src.ui.styles import AppStyles

class LoginFrame(ctk.CTkFrame):
    """Login screen for employee authentication."""
    
    def __init__(self, master, on_login_success: Callable[[Employee], None]):
        super().__init__(master)
        self.on_login_success = on_login_success
        
        # Configure padding
        self.pack_configure(padx=40, pady=40, fill="both", expand=True)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create all the widgets for the login screen."""
        # Title
        title = ctk.CTkLabel(
            self, 
            text="Acceso de Empleado", 
            font=AppStyles.TITLE_FONT
        )
        title.pack(pady=20)
        
        # Form fields
        self.emp_id_entry = FormField.create_field(
            self, "ID del Empleado", "Ingrese su ID"
        )
        
        self.emp_name_entry = FormField.create_field(
            self, "Nombre del Empleado", "Ingrese su nombre completo"
        )
        
        self.emp_role_entry = FormField.create_field(
            self, "Cargo o Rol", "Ingrese su cargo"
        )
        
        # Login button
        login_btn = StyledButton(
            self, 
            text="Ingresar al Sistema", 
            command=self._handle_login,
            button_type="primary"
        )
        login_btn.pack(pady=20)
        
        # Error message
        self.error_label = MessageLabel(self)
        self.error_label.pack()
    
    def _handle_login(self):
        """Handle login button click."""
        emp_id = self.emp_id_entry.get().strip()
        emp_name = self.emp_name_entry.get().strip()
        emp_role = self.emp_role_entry.get().strip()
        
        if not emp_id or not emp_name or not emp_role:
            self.error_label.show_error("Por favor completa todos los campos.")
            return
        
        # Create employee object
        employee = Employee(id=emp_id, name=emp_name, role=emp_role)
        
        # Call the success callback
        self.on_login_success(employee)
    
    def reset(self):
        """Reset the login form."""
        self.emp_id_entry.delete(0, "end")
        self.emp_name_entry.delete(0, "end")
        self.emp_role_entry.delete(0, "end")
        self.error_label.clear()