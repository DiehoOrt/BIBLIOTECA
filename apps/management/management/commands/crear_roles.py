from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea el grupo 'Bibliotecario' con sus permisos correspondientes."

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Bibliotecario")

        # CRUD completo sobre estos modelos
        modelos_crud = [
            ("alumnos",   "alumno"),
            ("libros",    "libro"),
            ("libros",    "autor"),
            ("libros",    "categoria"),
            ("libros",    "libroautor"),
            ("libros",    "librocategoria"),
            ("prestamos", "prestamo"),
        ]
        # Solo ver y modificar multas (no crear ni eliminar)
        modelos_multa = [
            ("multas", "multa"),
        ]

        permisos = []
        for app, model in modelos_crud:
            ct = ContentType.objects.get(app_label=app, model=model)
            for accion in ["add", "change", "delete", "view"]:
                permisos.append(
                    Permission.objects.get(content_type=ct, codename=f"{accion}_{model}")
                )
        for app, model in modelos_multa:
            ct = ContentType.objects.get(app_label=app, model=model)
            for accion in ["change", "view"]:
                permisos.append(
                    Permission.objects.get(content_type=ct, codename=f"{accion}_{model}")
                )

        group.permissions.set(permisos)

        accion = "creado" if created else "actualizado"
        self.stdout.write(self.style.SUCCESS(f'Grupo "Bibliotecario" {accion}.'))
        self.stdout.write(f"  Permisos asignados: {len(permisos)}")
        self.stdout.write("")
        self.stdout.write("Para asignar el rol a un usuario:")
        self.stdout.write("  Admin → Autenticación > Usuarios > [usuario] > Grupos > Bibliotecario")
        self.stdout.write("  El usuario debe tener is_staff=False e is_superuser=False.")
