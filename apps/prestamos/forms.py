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
# Licencia:  Software Propietario — Todos los derechos reservados.
#            Uso exclusivo autorizado a UNICAES-CRI bajo contrato.
# ================================================================
from datetime import date, timedelta
from django import forms
from .models import Prestamo
from apps.alumnos.models import Alumno
from apps.libros.models import Libro


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['alumno', 'libro', 'fecha_devolucion_esperada']
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-select'}),
            'libro':  forms.Select(attrs={'class': 'form-select'}),
            'fecha_devolucion_esperada': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alumno'].queryset = (
            Alumno.objects.filter(estado=Alumno.ESTADO_ACTIVO).order_by('apellido', 'nombre')
        )
        self.fields['libro'].queryset = (
            Libro.objects.filter(cantidad_disponible__gt=0).order_by('titulo')
        )
        if not self.initial.get('fecha_devolucion_esperada'):
            self.initial['fecha_devolucion_esperada'] = date.today() + timedelta(days=15)
