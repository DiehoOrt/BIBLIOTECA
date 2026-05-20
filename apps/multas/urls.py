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
from django.urls import path
from . import views

app_name = 'multas'

urlpatterns = [
    path('',              views.lista,  name='lista'),
    path('<int:pk>/pagar/', views.pagar, name='pagar'),
    path('<int:pk>/anular/', views.anular, name='anular'),
]
