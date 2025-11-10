from django import forms
from .models import Venta

class VentaForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Venta
        fields = ['fecha', 'producto_servicio', 'monto', 'cliente']
        widgets = {
            'producto_servicio': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['cliente'].queryset = user.clientes.all()
