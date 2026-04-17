from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Multa

_solo_admin = user_passes_test(lambda u: u.is_superuser, login_url='dashboard')


@login_required
def lista(request):
    estado = request.GET.get('estado', '')
    q      = request.GET.get('q', '').strip()
    multas = Multa.objects.select_related('prestamo__alumno', 'prestamo__libro').order_by('-id')
    if estado:
        multas = multas.filter(estado=estado)
    if q:
        multas = (
            Multa.objects.filter(prestamo__alumno__apellido__icontains=q)
            | Multa.objects.filter(prestamo__alumno__nombre__icontains=q)
            | Multa.objects.filter(prestamo__alumno__carnet__icontains=q)
        ).select_related('prestamo__alumno', 'prestamo__libro')
    return render(request, 'multas/lista.html', {
        'multas': multas.distinct(),
        'estado': estado,
        'q':      q,
    })


@login_required
def pagar(request, pk):
    if request.method == 'POST':
        multa = get_object_or_404(Multa, pk=pk)
        multa.estado     = Multa.ESTADO_PAGADA
        multa.fecha_pago = date.today()
        multa.save()
        messages.success(request, f'Multa #{multa.pk} marcada como pagada.')
    return redirect('multas:lista')


@_solo_admin
def anular(request, pk):
    if request.method == 'POST':
        multa = get_object_or_404(Multa, pk=pk)
        multa.estado = Multa.ESTADO_ANULADA
        multa.save()
        messages.success(request, f'Multa #{multa.pk} anulada.')
    return redirect('multas:lista')
