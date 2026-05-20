# ================================================================
# Proyecto:  SGBU — Sistema de Gestión Bibliotecaria UNICAES
# Versión:   1.0.0
# País:      El Salvador
# Año:       2026
# Empresa:   InnoByte
# Autores:   Jonathan Fuentes Henriquez, Andrew Enrique Mercado,
#            Hector Jhosue Ramos, Enzo Howard Rivera,
#            Diego Josue Ortiz, Alejandra Marisol,
#            Nathaly Portillo, Roberto Leonel Dominguez
# Licencia:  MIT License
# ================================================================
from django import forms
from .models import Alumno


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'carnet', 'email', 'estado']
        widgets = {
            'nombre':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'carnet':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej. 2024-001'}),
            'email':    forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@unicaes.edu.sv'}),
            'estado':   forms.Select(attrs={'class': 'form-select'}),
        }
