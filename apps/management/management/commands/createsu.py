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
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Crea un superusuario automáticamente'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email    = os.environ.get('DJANGO_SUPERUSER_EMAIL',    'admin@gmail.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" creado exitosamente!'))
        else:
            self.stdout.write(self.style.WARNING(f'El superusuario "{username}" ya existe'))
