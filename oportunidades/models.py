from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente

class Oportunidad(models.Model):
    ETAPA_CHOICES = [
        ('contactado', 'Contactado'),
        ('negociacion', 'En Negociación'),
        ('cerrado', 'Cerrado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    etapa = models.CharField(max_length=15, choices=ETAPA_CHOICES, default='contactado')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='oportunidades', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oportunidades')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    recordatorio = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.titulo
