from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cita(models.Model):
    PENDIENTE = 'P'
    CONFIRMADA = 'C'
    CANCELADA = 'X'
    ESTADOS_CITA = [
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADA, 'Confirmada'),
        (CANCELADA, 'Cancelada'),
    ]
    titulo = models.CharField(max_length=100)
    motivo = models.TextField(max_length=100)
    fecha = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=1,
        choices=ESTADOS_CITA,
        default=PENDIENTE,
    )
    solicitada = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return ' ' + self.titulo + ' - ' + self.user.username
    

class Horario(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.fecha} - {self.hora_inicio} a {self.hora_fin}"
