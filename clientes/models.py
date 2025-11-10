from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    ESTADO_CHOICES = [
        ('prospecto', 'Prospecto'),
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(unique=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='prospecto')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clientes')

    def __str__(self):
        return self.nombre
