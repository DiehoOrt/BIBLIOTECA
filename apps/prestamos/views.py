from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PrestamoForm
from .models import Prestamo
from apps.multas.models import Multa


@login_required
def lista(request):
    estado = request.GET.get('estado', '')
    q      = request.GET.get('q', '').strip()
    prestamos = Prestamo.objects.select_related('alumno', 'libro').order_by('-fecha_prestamo')
    if estado:
        prestamos = prestamos.filter(estado=estado)
    if q:
        prestamos = (
            Prestamo.objects.filter(alumno__apellido__icontains=q)
            | Prestamo.objects.filter(alumno__nombre__icontains=q)
            | Prestamo.objects.filter(alumno__carnet__icontains=q)
            | Prestamo.objects.filter(libro__titulo__icontains=q)
        ).select_related('alumno', 'libro')
    return render(request, 'prestamos/lista.html', {
        'prestamos': prestamos.distinct(),
        'estado':    estado,
        'q':         q,
    })


@login_required
def crear(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            alumno = form.cleaned_data['alumno']
            if Multa.objects.filter(prestamo__alumno=alumno, estado=Multa.ESTADO_PENDIENTE).exists():
                form.add_error('alumno', 'Este alumno tiene multas pendientes. Debe saldarlas primero.')
            else:
                form.save()
                messages.success(request, 'Préstamo registrado exitosamente.')
                return redirect('prestamos:lista')
    else:
        form = PrestamoForm()
    return render(request, 'prestamos/form.html', {
        'form':             form,
        'titulo':           'Nuevo préstamo',
        'accion':           'Registrar',
        'sin_alumnos':      not form.fields['alumno'].queryset.exists(),
        'ultimos_prestamos': Prestamo.objects.select_related('alumno', 'libro').order_by('-fecha_prestamo')[:5],
    })


@login_required
def devolver(request, pk):
    prestamo = get_object_or_404(
        Prestamo.objects.select_related('alumno', 'libro'),
        pk=pk
    )

    if prestamo.estado == Prestamo.ESTADO_DEVUELTO:
        messages.warning(request, 'Este préstamo ya fue devuelto.')
        return redirect('prestamos:lista')

    hoy = date.today()
    con_retraso = hoy > prestamo.fecha_devolucion_esperada
    dias_retraso = (hoy - prestamo.fecha_devolucion_esperada).days if con_retraso else 0
    multa_estimada = round(dias_retraso * 1.00, 2)

    if request.method == 'POST':
        from datetime import datetime
        fecha_str = request.POST.get('fecha_devolucion_real') or str(hoy)
        prestamo.fecha_devolucion_real = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        prestamo.save()
        messages.success(request, f'Devolución registrada para "{prestamo.libro.titulo}".')
        return redirect('prestamos:lista')

    return render(request, 'prestamos/devolver.html', {
        'prestamo':       prestamo,
        'hoy':            hoy,
        'con_retraso':    con_retraso,
        'dias_retraso':   dias_retraso,
        'multa_estimada': multa_estimada,
    })
