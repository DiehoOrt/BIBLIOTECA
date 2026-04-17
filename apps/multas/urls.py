from django.urls import path
from . import views

app_name = 'multas'

urlpatterns = [
    path('',              views.lista,  name='lista'),
    path('<int:pk>/pagar/', views.pagar, name='pagar'),
    path('<int:pk>/anular/', views.anular, name='anular'),
]
