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
    
    HOMBRE = 'Hombre'
    MUJER = 'Mujer'
    PREFIERO_NO_DECIRLO = 'Prefiero no decirlo'
    GENERO = [
        (HOMBRE, 'Hombre'),
        (MUJER, 'Mujer'),
        (PREFIERO_NO_DECIRLO, 'Prefiero no decirlo'),
    ]
# Create your models here.
class Cita(models.Model):
    PENDIENTE = 'Pendiente'
    CONFIRMADA = 'Confirmada'
    DECLINADA = 'Declinada'
    ESTADOS_CITA = [
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADA, 'Confirmada'),
        (DECLINADA, 'Declinada'),
    ]
    
    HOMBRE = 'Hombre'
    MUJER = 'Mujer'
    PREFIERO_NO_DECIRLO = 'Prefiero no decirlo'
    GENERO = [
        (HOMBRE, 'Hombre'),
        (MUJER, 'Mujer'),
        (PREFIERO_NO_DECIRLO, 'Prefiero no decirlo'),
    ]
    
    INGENIERIA_CIVIL = 'Ingenieria Civil'
    INGENIERIA_ELECTRONICA = 'Ingenieria en Electronica'
    INGENIERIA_COMPUTACION = 'Ingenieria en Computacion'
    INGENIERIA_INDUSTRIAL = 'Ingenieria Industrial'
    INGENIERIA_NANOTECNOLOGIA = 'Ingenieria en Nanatecnologia'
    INGENIERIA_SOFTWARE = 'Ingenieria en Software'
    BIOINGENIERIA = 'Bioingenieria'
    ARQUITECTURA = 'Arquitectura'
    CARRERAS = [
        (INGENIERIA_CIVIL,  'Ingenieria Civil'),
        (INGENIERIA_ELECTRONICA,  'Ingenieria en Electronica'),
        (INGENIERIA_COMPUTACION,  'Ingenieria en Computacion'),
        (INGENIERIA_INDUSTRIAL,  'Ingenieria Industrial'),
        (INGENIERIA_NANOTECNOLOGIA,  'Ingenieria en Nanotecnologia'),
        (INGENIERIA_SOFTWARE,  'Ingenieria en Software y Tecnologias Emergentes'),
        (BIOINGENIERIA,  'Bioingenieria'),
        (ARQUITECTURA,  'Arquitectura'),
    ]
    
    ACADEMICA = 'Academica'
    PERSONAL = 'Personal'
    VOCACIONAL = 'Vocacional'
    BAJA = 'Baja'
    PSICOLOGICA = 'Psicologica'
    ASUNTOS = [
        (ACADEMICA, 'Academica'),
        (PERSONAL, 'Personal'),
        (VOCACIONAL, 'Vocacional'),
        (BAJA, 'Baja'),
        (PSICOLOGICA, 'Psicologica'),
    ]
    
    matricula = models.CharField(max_length=8)
    apellido_paterno = models.CharField(max_length=20)
    apellido_materno = models.CharField(max_length=20)
    nombre = models.CharField(max_length=40)
    descripcion = models.TextField(max_length = 200)
    semestre = models.CharField(max_length = 2)
    fecha = models.DateTimeField()
    comentarios = models.TextField(
        max_length = 200,
        default = "No hay comentarios."
        )
    
    sexo = models.CharField(
        max_length = 20,
        choices = GENERO,
        default = PREFIERO_NO_DECIRLO,
    )
    
    estado = models.CharField(
        max_length=11,
        choices=ESTADOS_CITA,
        default=PENDIENTE,
    )
    
    carrera = models.CharField(
        max_length=50,
        choices = CARRERAS,
        default = INGENIERIA_SOFTWARE
    )
    
    asunto = models.CharField(
        max_length=50,
        choices = ASUNTOS,
        default = ACADEMICA
    )
    
    solicitada = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return ' ' + self.asunto + ' - ' + self.user.username
    
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
