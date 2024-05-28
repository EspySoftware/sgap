from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateformat import format

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

    PRIMERO = '1'
    SEGUNDO = '2'
    TERCERO = '3'
    CUARTO = '4'
    QUINTO = '5'
    SEXTO = '6'
    SEPTIMO = '7'
    OCTAVO = '8'
    NOVENO = '9'
    SEMESTRES = [
        (PRIMERO, '1'),
        (SEGUNDO, '2'),
        (TERCERO, '3'),
        (CUARTO, '4'),
        (QUINTO, '5'),
        (SEXTO, '6'),
        (SEPTIMO, '7'),
        (OCTAVO, '8'),
        (NOVENO, '9'),
    ]

    matricula = models.CharField(max_length=8)
    apellido_paterno = models.CharField(max_length=20)
    apellido_materno = models.CharField(max_length=20)
    nombre = models.CharField(max_length=40)
    descripcion = models.TextField(max_length=200)
    fecha = models.DateTimeField()
    semestre = models.CharField(
        max_length=2,
        choices=SEMESTRES,
        default=PRIMERO
    )

    comentarios = models.TextField(
        max_length=200,
        default="No hay comentarios."
    )

    sexo = models.CharField(
        max_length=20,
        choices=GENERO,
        default=PREFIERO_NO_DECIRLO,
    )

    estado = models.CharField(
        max_length=11,
        choices=ESTADOS_CITA,
        default=PENDIENTE,
    )

    carrera = models.CharField(
        max_length=50,
        choices=CARRERAS,
        default=INGENIERIA_SOFTWARE
    )

    asunto = models.CharField(
        max_length=50,
        choices=ASUNTOS,
        default=ACADEMICA
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
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='disponible')

    def __str__(self):
        inicio_local = timezone.localtime(self.inicio)
        fin_local = timezone.localtime(self.fin)
        return format(inicio_local, 'l d') + " de " + format(inicio_local, 'F: H:i') + " - " + format(fin_local, 'H:i')