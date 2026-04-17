from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import LibroForm, CategoriaForm, AutorForm
from .models import Libro, Autor, Categoria, LibroAutor, LibroCategoria
from apps.prestamos.models import Prestamo


@login_required
def lista(request):
    q = request.GET.get('q', '').strip()
    libros = Libro.objects.prefetch_related('autores', 'categorias').order_by('titulo')
    if q:
        libros = (
            Libro.objects.filter(titulo__icontains=q)
            | Libro.objects.filter(autores__apellido__icontains=q)
            | Libro.objects.filter(isbn__icontains=q)
            | Libro.objects.filter(categorias__nombre__icontains=q)
        ).prefetch_related('autores', 'categorias')
    return render(request, 'libros/lista.html', {
        'libros': libros.distinct(),
        'q':      q,
    })


def catalogo(request):
    q            = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    libros = Libro.objects.prefetch_related('autores', 'categorias').order_by('titulo')
    if q:
        libros = (
            Libro.objects.filter(titulo__icontains=q)
            | Libro.objects.filter(autores__apellido__icontains=q)
        ).prefetch_related('autores', 'categorias')
    if categoria_id:
        libros = libros.filter(categorias__pk=categoria_id)
    return render(request, 'libros/catalogo.html', {
        'libros':       libros.distinct(),
        'categorias':   Categoria.objects.all(),
        'q':            q,
        'categoria_id': categoria_id,
    })


@login_required
def detalle(request, pk):
    libro = get_object_or_404(
        Libro.objects.prefetch_related('autores', 'categorias'), pk=pk
    )
    hoy = date.today()
    en_poder = (
        Prestamo.objects
        .filter(libro=libro, estado__in=[Prestamo.ESTADO_ACTIVO, Prestamo.ESTADO_VENCIDO])
        .select_related('alumno')
        .order_by('fecha_devolucion_esperada')
    )
    historial = (
        Prestamo.objects
        .filter(libro=libro, estado=Prestamo.ESTADO_DEVUELTO)
        .select_related('alumno')
        .order_by('-fecha_devolucion_real')[:20]
    )
    return render(request, 'libros/detalle.html', {
        'libro':    libro,
        'en_poder': en_poder,
        'historial': historial,
        'hoy':      hoy,
    })


@login_required
def crear(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save()
            for autor in form.cleaned_data.get('autores_sel', []):
                LibroAutor.objects.get_or_create(libro=libro, autor=autor)
            for cat in form.cleaned_data.get('categorias_sel', []):
                LibroCategoria.objects.get_or_create(libro=libro, categoria=cat)
            messages.success(request, f'Libro "{libro}" creado exitosamente.')
            return redirect('libros:detalle', pk=libro.pk)
    else:
        form = LibroForm()
    return render(request, 'libros/form.html', {
        'form':          form,
        'titulo':        'Nuevo libro',
        'accion':        'Crear',
        'ultimos_libros': Libro.objects.order_by('-pk')[:5],
    })


@login_required
def editar(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            LibroAutor.objects.filter(libro=libro).delete()
            LibroCategoria.objects.filter(libro=libro).delete()
            for autor in form.cleaned_data.get('autores_sel', []):
                LibroAutor.objects.get_or_create(libro=libro, autor=autor)
            for cat in form.cleaned_data.get('categorias_sel', []):
                LibroCategoria.objects.get_or_create(libro=libro, categoria=cat)
            messages.success(request, 'Libro actualizado exitosamente.')
            return redirect('libros:detalle', pk=libro.pk)
    else:
        form = LibroForm(instance=libro, initial={
            'autores_sel':    libro.autores.all(),
            'categorias_sel': libro.categorias.all(),
        })
    return render(request, 'libros/form.html', {
        'form':          form,
        'titulo':        f'Editar: {libro.titulo}',
        'accion':        'Guardar cambios',
        'libro':         libro,
        'ultimos_libros': Libro.objects.exclude(pk=pk).order_by('-pk')[:5],
    })


@login_required
def eliminar(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    prestamos = libro.prestamos.select_related('alumno')
    bloqueado = prestamos.exists()

    if request.method == 'POST':
        if bloqueado:
            messages.error(request, 'No se puede eliminar: el libro tiene préstamos registrados.')
            return redirect('libros:eliminar', pk=pk)
        titulo = libro.titulo
        libro.delete()
        messages.success(request, f'Libro "{titulo}" eliminado.')
        return redirect('libros:lista')

    return render(request, 'libros/confirmar_eliminar.html', {
        'libro':     libro,
        'prestamos': prestamos,
        'bloqueado': bloqueado,
    })


# ── Categorías ────────────────────────────────────────────

@login_required
def categorias_lista(request):
    categorias = Categoria.objects.order_by('nombre')
    return render(request, 'libros/categorias_lista.html', {'categorias': categorias})


@login_required
def categorias_crear(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f'Categoría "{cat.nombre}" creada.')
            return redirect('libros:categorias_lista')
    else:
        form = CategoriaForm()
    return render(request, 'libros/categorias_form.html', {
        'form':   form,
        'titulo': 'Nueva categoría',
        'accion': 'Crear',
    })


@login_required
def categorias_editar(request, pk):
    cat = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, f'Categoría "{cat.nombre}" actualizada.')
            return redirect('libros:categorias_lista')
    else:
        form = CategoriaForm(instance=cat)
    return render(request, 'libros/categorias_form.html', {
        'form':       form,
        'titulo':     f'Editar: {cat.nombre}',
        'accion':     'Guardar cambios',
        'categoria':  cat,
    })


@login_required
def categorias_eliminar(request, pk):
    cat = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre = cat.nombre
        cat.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada.')
        return redirect('libros:categorias_lista')
    return render(request, 'libros/categorias_confirmar_eliminar.html', {'categoria': cat})


# ── Autores ───────────────────────────────────────────────

@login_required
def autores_lista(request):
    autores = Autor.objects.order_by('apellido', 'nombre')
    return render(request, 'libros/autores_lista.html', {'autores': autores})


@login_required
def autores_crear(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            autor = form.save()
            messages.success(request, f'Autor "{autor}" creado.')
            return redirect('libros:autores_lista')
    else:
        form = AutorForm()
    return render(request, 'libros/autores_form.html', {
        'form':   form,
        'titulo': 'Nuevo autor',
        'accion': 'Crear',
    })


@login_required
def autores_editar(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Autor "{autor}" actualizado.')
            return redirect('libros:autores_lista')
    else:
        form = AutorForm(instance=autor)
    return render(request, 'libros/autores_form.html', {
        'form':   form,
        'titulo': f'Editar: {autor}',
        'accion': 'Guardar cambios',
        'autor':  autor,
    })


@login_required
def autores_eliminar(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    libros = autor.libros.all()
    if request.method == 'POST':
        nombre = str(autor)
        autor.delete()
        messages.success(request, f'Autor "{nombre}" eliminado.')
        return redirect('libros:autores_lista')
    return render(request, 'libros/autores_confirmar_eliminar.html', {
        'autor':  autor,
        'libros': libros,
    })
