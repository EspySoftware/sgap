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
<<<<<<< Updated upstream


class Horario(models.Model):
    agendado ='a'
=======
    
class Horario(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('no_disponible', 'No disponible'),
        ('cita_agendada', 'Cita agendada'),
    ]
    
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    
    def __str__(self):
        return f"{self.inicio} - {self.fin}: {self.get_estado_display()}"
>>>>>>> Stashed changes
