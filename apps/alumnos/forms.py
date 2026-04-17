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
