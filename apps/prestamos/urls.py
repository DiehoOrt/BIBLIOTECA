from django.urls import path
from . import views

app_name = 'prestamos'

urlpatterns = [
    path('',                     views.lista,    name='lista'),
    path('nuevo/',               views.crear,    name='crear'),
    path('<int:pk>/devolver/',   views.devolver, name='devolver'),
]
