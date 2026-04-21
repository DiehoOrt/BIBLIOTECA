from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AlumnoForm
from .models import Alumno
from apps.prestamos.models import Prestamo
from apps.multas.models import Multa


@login_required
def lista(request):
    q      = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')
    alumnos = Alumno.objects.order_by('apellido', 'nombre')
    if q:
        alumnos = alumnos.filter(nombre__icontains=q) \
                  | Alumno.objects.filter(apellido__icontains=q) \
                  | Alumno.objects.filter(carnet__icontains=q)
    if estado:
        alumnos = alumnos.filter(estado=estado)
    return render(request, 'alumnos/lista.html', {
        'alumnos': alumnos.distinct(),
        'q':       q,
        'estado':  estado,
    })


@login_required
def perfil(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    activos = (
        Prestamo.objects
        .filter(alumno=alumno, estado__in=[Prestamo.ESTADO_ACTIVO, Prestamo.ESTADO_VENCIDO])
        .select_related('libro')
        .order_by('fecha_devolucion_esperada')
    )
    multas_pendientes = (
        Multa.objects
        .filter(prestamo__alumno=alumno, estado=Multa.ESTADO_PENDIENTE)
        .select_related('prestamo__libro')
    )
    historial = (
        Prestamo.objects
        .filter(alumno=alumno, estado=Prestamo.ESTADO_DEVUELTO)
        .select_related('libro')
        .order_by('-fecha_devolucion_real')[:15]
    )
    return render(request, 'alumnos/perfil.html', {
        'alumno':            alumno,
        'activos':           activos,
        'multas_pendientes': multas_pendientes,
        'historial':         historial,
    })


def _ultimos_alumnos(excluir_pk=None):
    qs = Alumno.objects.order_by('-fecha_inscripcion', '-pk')
    if excluir_pk:
        qs = qs.exclude(pk=excluir_pk)
    return qs[:8]


@login_required
def crear(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save()
            messages.success(request, f'Alumno "{alumno}" creado exitosamente.')
            return redirect('alumnos:perfil', pk=alumno.pk)
    else:
        form = AlumnoForm()
    return render(request, 'alumnos/form.html', {
        'form':            form,
        'titulo':          'Nuevo alumno',
        'accion':          'Crear',
        'ultimos_alumnos': _ultimos_alumnos(),
    })


@login_required
def editar(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alumno actualizado exitosamente.')
            return redirect('alumnos:perfil', pk=alumno.pk)
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, 'alumnos/form.html', {
        'form':            form,
        'titulo':          f'Editar: {alumno}',
        'accion':          'Guardar cambios',
        'alumno':          alumno,
        'ultimos_alumnos': _ultimos_alumnos(excluir_pk=pk),
    })


@login_required
def eliminar(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    prestamos = alumno.prestamos.select_related('libro')
    bloqueado = prestamos.exists()

    if request.method == 'POST':
        if bloqueado:
            messages.error(request, 'No se puede eliminar: el alumno tiene préstamos registrados.')
            return redirect('alumnos:eliminar', pk=pk)
        nombre = str(alumno)
        alumno.delete()
        messages.success(request, f'Alumno "{nombre}" eliminado.')
        return redirect('alumnos:lista')

    return render(request, 'alumnos/confirmar_eliminar.html', {
        'alumno':    alumno,
        'prestamos': prestamos,
        'bloqueado': bloqueado,
    }) 
    # hola mundo solo es una prueba de nada 