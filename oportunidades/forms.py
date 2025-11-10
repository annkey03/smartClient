from django import forms
from .models import Oportunidad

class OportunidadForm(forms.ModelForm):
    recordatorio = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Oportunidad
        fields = ['titulo', 'descripcion', 'etapa', 'cliente', 'recordatorio']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['cliente'].queryset = user.clientes.all()
            self.fields['cliente'].required = False
