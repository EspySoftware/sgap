from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cita(models.Model):
    PENDIENTE = 'Pendiente'
    CONFIRMADA = 'Confirmada'
    CANCELADA = 'Declinada'
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
        max_length=11,
        choices=ESTADOS_CITA,
        default=PENDIENTE,
    )
    solicitada = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return ' ' + self.titulo + ' - ' + self.user.username


class Horario(models.Model):
    agendado ='a'