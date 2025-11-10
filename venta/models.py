from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente

class Venta(models.Model):
    fecha = models.DateField()
    producto_servicio = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta de {self.producto_servicio} a {self.cliente.nombre}"
