from django.urls import path
from . import views

app_name = 'libros'

urlpatterns = [
    path('',                  views.lista,    name='lista'),
    path('nuevo/',            views.crear,    name='crear'),
    path('catalogo/',         views.catalogo, name='catalogo'),
    path('<int:pk>/',         views.detalle,  name='detalle'),
    path('<int:pk>/editar/',  views.editar,   name='editar'),
    path('<int:pk>/eliminar/', views.eliminar, name='eliminar'),

    # Categorías
    path('categorias/',                      views.categorias_lista,    name='categorias_lista'),
    path('categorias/nueva/',                views.categorias_crear,    name='categorias_crear'),
    path('categorias/<int:pk>/editar/',      views.categorias_editar,   name='categorias_editar'),
    path('categorias/<int:pk>/eliminar/',    views.categorias_eliminar, name='categorias_eliminar'),

    # Autores
    path('autores/',                         views.autores_lista,    name='autores_lista'),
    path('autores/nuevo/',                   views.autores_crear,    name='autores_crear'),
    path('autores/<int:pk>/editar/',         views.autores_editar,   name='autores_editar'),
    path('autores/<int:pk>/eliminar/',       views.autores_eliminar, name='autores_eliminar'),
]
