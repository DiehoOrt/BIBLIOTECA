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
from django.urls import path
from . import views

app_name = 'prestamos'

urlpatterns = [
    path('',                     views.lista,    name='lista'),
    path('nuevo/',               views.crear,    name='crear'),
    path('<int:pk>/devolver/',   views.devolver, name='devolver'),
]
