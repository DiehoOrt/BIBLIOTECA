from django.db import models
from apps.prestamos.models import Prestamo


class Multa(models.Model):
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_PAGADA = "pagada"
    ESTADO_ANULADA = "anulada"
    ESTADOS = [
        (ESTADO_PENDIENTE, "Pendiente"),
        (ESTADO_PAGADA, "Pagada"),
        (ESTADO_ANULADA, "Anulada"),
    ]

    prestamo = models.OneToOneField(Prestamo, on_delete=models.PROTECT, related_name="multa")
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    fecha_pago = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Multa"
        verbose_name_plural = "Multas"
        ordering = ["-id"]

    def __str__(self):
        return f"Multa #{self.pk} - {self.prestamo} / ${self.monto}"
