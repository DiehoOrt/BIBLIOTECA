from django.db import models


class Alumno(models.Model):
    ESTADO_ACTIVO = "activo"
    ESTADO_INACTIVO = "inactivo"
    ESTADO_SUSPENDIDO = "suspendido"
    ESTADOS = [
        (ESTADO_ACTIVO, "Activo"),
        (ESTADO_INACTIVO, "Inactivo"),
        (ESTADO_SUSPENDIDO, "Suspendido"),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    carnet = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_ACTIVO)

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.carnet})"
