from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Reporte
        fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
