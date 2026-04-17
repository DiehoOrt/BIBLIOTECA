from django import forms
from .models import Libro, Autor, Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre':      forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'apellido']
        widgets = {
            'nombre':   forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LibroForm(forms.ModelForm):
    autores_sel = forms.ModelMultipleChoiceField(
        queryset=Autor.objects.order_by('apellido', 'nombre'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Autores',
    )
    categorias_sel = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.order_by('nombre'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Categorías',
    )

    class Meta:
        model = Libro
        fields = [
            'titulo', 'isbn', 'anio_publicacion',
            'cantidad_total', 'cantidad_disponible',
            'descripcion', 'portada',
        ]
        widgets = {
            'titulo':              forms.TextInput(attrs={'class': 'form-control'}),
            'isbn':                forms.TextInput(attrs={'class': 'form-control'}),
            'anio_publicacion':    forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_total':      forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'descripcion':         forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'portada':             forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
