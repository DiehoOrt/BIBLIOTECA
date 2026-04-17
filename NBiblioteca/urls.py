from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views
from apps.libros.views import catalogo as catalogo_view

urlpatterns = [
    # Admin Django (solo usuarios y permisos)
    path('admin/', admin.site.urls),

    # Dashboard (raíz)
    path('', views.dashboard, name='dashboard'),
    path('reportes/morosos/', views.reporte_morosos, name='reporte_morosos'),

    # Catálogo público (sin login)
    path('catalogo/', catalogo_view, name='catalogo'),

    # Auth
    path('login/',  auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Apps
    path('libros/',    include('apps.libros.urls',    namespace='libros')),
    path('alumnos/',   include('apps.alumnos.urls',   namespace='alumnos')),
    path('prestamos/', include('apps.prestamos.urls', namespace='prestamos')),
    path('multas/',    include('apps.multas.urls',    namespace='multas')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [

    # Catch-all — página 404 personalizada
    path('<path:ruta>', views.pagina_404, name='404'),
]
