import csv
import json
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from apps.alumnos.models import Alumno
from apps.libros.models import Libro
from apps.prestamos.models import Prestamo
from apps.multas.models import Multa


def _ultimos_6_meses():
    hoy = date.today()
    meses = []
    for i in range(5, -1, -1):
        d = date(hoy.year, hoy.month, 1)
        # retroceder i meses
        mes = d.month - i
        anio = d.year
        while mes <= 0:
            mes += 12
            anio -= 1
        meses.append(date(anio, mes, 1))
    return meses


@login_required
def dashboard(request):
    hoy = date.today()

    # ── Estadísticas generales ─────────────────────────────────────────
    stats = {
        'total_libros':       Libro.objects.count(),
        'total_alumnos':      Alumno.objects.count(),
        'prestamos_activos':  Prestamo.objects.filter(estado=Prestamo.ESTADO_ACTIVO).count(),
        'prestamos_vencidos': Prestamo.objects.filter(estado=Prestamo.ESTADO_VENCIDO).count(),
        'multas_pendientes':  Multa.objects.filter(estado=Multa.ESTADO_PENDIENTE).count(),
        'monto_multas':       Multa.objects.filter(
                                  estado=Multa.ESTADO_PENDIENTE
                              ).aggregate(t=Sum('monto'))['t'] or 0,
    }

    # ── Tablas de la vista ─────────────────────────────────────────────
    vencidos = (
        Prestamo.objects
        .filter(estado=Prestamo.ESTADO_VENCIDO)
        .select_related('alumno', 'libro')
        .order_by('fecha_devolucion_esperada')[:10]
    )
    proximos = (
        Prestamo.objects
        .filter(
            estado=Prestamo.ESTADO_ACTIVO,
            fecha_devolucion_esperada__range=[hoy, hoy + timedelta(days=3)],
        )
        .select_related('alumno', 'libro')
        .order_by('fecha_devolucion_esperada')
    )

    # ── Datos para los charts ──────────────────────────────────────────
    meses = _ultimos_6_meses()
    labels_meses = [m.strftime('%b %Y') for m in meses]

    # Chart 1: Préstamos vs Devoluciones por mes
    prestamos_mes = {
        r['mes']: r['total']
        for r in (
            Prestamo.objects
            .annotate(mes=TruncMonth('fecha_prestamo'))
            .values('mes')
            .annotate(total=Count('id'))
        )
    }
    devueltos_mes = {
        r['mes']: r['total']
        for r in (
            Prestamo.objects
            .filter(fecha_devolucion_real__isnull=False)
            .annotate(mes=TruncMonth('fecha_devolucion_real'))
            .values('mes')
            .annotate(total=Count('id'))
        )
    }
    chart_area = json.dumps({
        'labels':       labels_meses,
        'prestamos':    [prestamos_mes.get(m, 0) for m in meses],
        'devoluciones': [devueltos_mes.get(m, 0) for m in meses],
    })

    # Chart 2: Estado de préstamos (donut)
    estados_qs = (
        Prestamo.objects
        .values('estado')
        .annotate(total=Count('id'))
    )
    estado_map = {r['estado']: r['total'] for r in estados_qs}
    chart_estados = json.dumps({
        'labels': ['Devuelto', 'Activo', 'Vencido'],
        'data':   [
            estado_map.get(Prestamo.ESTADO_DEVUELTO, 0),
            estado_map.get(Prestamo.ESTADO_ACTIVO,   0),
            estado_map.get(Prestamo.ESTADO_VENCIDO,  0),
        ],
    })

    # Chart 3: Top 5 libros más prestados
    top_libros = (
        Prestamo.objects
        .values('libro__titulo')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )
    chart_libros = json.dumps({
        'labels': [r['libro__titulo'][:30] for r in top_libros],
        'data':   [r['total'] for r in top_libros],
    })

    # Chart 4: Evolución por estado (stacked line últimos 6 meses)
    lineas_qs = (
        Prestamo.objects
        .annotate(mes=TruncMonth('fecha_prestamo'))
        .values('mes', 'estado')
        .annotate(total=Count('id'))
    )
    lineas_map = {}
    for r in lineas_qs:
        lineas_map[(r['mes'], r['estado'])] = r['total']

    chart_lineas = json.dumps({
        'labels':   labels_meses,
        'devuelto': [lineas_map.get((m, Prestamo.ESTADO_DEVUELTO), 0) for m in meses],
        'activo':   [lineas_map.get((m, Prestamo.ESTADO_ACTIVO),   0) for m in meses],
        'vencido':  [lineas_map.get((m, Prestamo.ESTADO_VENCIDO),  0) for m in meses],
    })

    # Chart 5: Estado de multas (donut)
    multas_qs = (
        Multa.objects
        .values('estado')
        .annotate(total=Count('id'))
    )
    multa_map = {r['estado']: r['total'] for r in multas_qs}
    chart_multas = json.dumps({
        'labels': ['Pendiente', 'Pagada', 'Anulada'],
        'data':   [
            multa_map.get(Multa.ESTADO_PENDIENTE, 0),
            multa_map.get(Multa.ESTADO_PAGADA,    0),
            multa_map.get(Multa.ESTADO_ANULADA,   0),
        ],
    })

    # Chart 6: Ingresos por multas pagadas por mes
    ingresos_qs = {
        r['mes']: float(r['total'] or 0)
        for r in (
            Multa.objects
            .filter(estado=Multa.ESTADO_PAGADA, fecha_pago__isnull=False)
            .annotate(mes=TruncMonth('fecha_pago'))
            .values('mes')
            .annotate(total=Sum('monto'))
        )
    }
    ingresos_data = [ingresos_qs.get(m, 0) for m in meses]
    chart_ingresos = json.dumps({
        'labels': labels_meses,
        'data':   ingresos_data,
    })
    chart_ingresos_total = round(sum(ingresos_data), 2)

    return render(request, 'dashboard.html', {
        'hoy':                  hoy,
        'stats':                stats,
        'vencidos':             vencidos,
        'proximos':             proximos,
        'chart_area':           chart_area,
        'chart_estados':        chart_estados,
        'chart_libros':         chart_libros,
        'chart_lineas':         chart_lineas,
        'chart_multas':         chart_multas,
        'chart_ingresos':       chart_ingresos,
        'chart_ingresos_total': chart_ingresos_total,
    })


def pagina_404(request, *args, **kwargs):
    return HttpResponseNotFound(
        render(request, '404.html').content
    )


@login_required
def reporte_morosos(request):
    hoy = date.today()

    vencidos = (
        Prestamo.objects
        .filter(estado=Prestamo.ESTADO_VENCIDO)
        .select_related('alumno', 'libro')
        .order_by('alumno__apellido', 'alumno__nombre')
    )

    multas = (
        Multa.objects
        .filter(estado=Multa.ESTADO_PENDIENTE)
        .select_related('prestamo__alumno', 'prestamo__libro')
        .order_by('prestamo__alumno__apellido', 'prestamo__alumno__nombre')
    )

    total_multas = multas.aggregate(t=Sum('monto'))['t'] or 0

    # Descarga CSV si se solicita
    if request.GET.get('formato') == 'csv':
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = (
            f'attachment; filename="morosos_{hoy}.csv"'
        )
        response.write('\ufeff')
        writer = csv.writer(response)
        writer.writerow([
            'Carnet', 'Apellido', 'Nombre', 'Email',
            'Libro', 'Fecha préstamo', 'Fecha vencimiento',
            'Días de atraso', 'Monto ($)', 'Motivo',
        ])
        for m in multas:
            p = m.prestamo
            dias = max(0, (hoy - p.fecha_devolucion_esperada).days)
            writer.writerow([
                p.alumno.carnet, p.alumno.apellido, p.alumno.nombre,
                p.alumno.email, p.libro.titulo,
                p.fecha_prestamo, p.fecha_devolucion_esperada,
                dias, m.monto, m.motivo,
            ])
        return response

    return render(request, 'reporte_morosos.html', {
        'hoy':          hoy,
        'vencidos':     vencidos,
        'multas':       multas,
        'total_multas': total_multas,
    })
