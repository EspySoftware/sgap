from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cita(models.Model):
    titulo = models.CharField(max_length=100)
    motivo = models.TextField(max_length=100)
    fecha = models.DateTimeField()
    estado = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return ' ' + self.titulo + ' - ' + self.user.username