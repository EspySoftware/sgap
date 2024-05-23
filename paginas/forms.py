from django.forms import ModelForm
from .models import Cita, Horario
from django import forms
from .models import Cita

class FormularioCita(ModelForm):
    class Meta:
        model = Cita
        fields = ['matricula', 'apellido_paterno', 'apellido_materno', 'nombre', 'sexo', 'semestre', 'carrera', 'asunto', 'descripcion', 'fecha', 'estado', 'comentarios']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea,
            'sexo': forms.Select(choices=Cita.GENERO),
            'carrera': forms.Select(choices=Cita.CARRERAS),
            'asunto': forms.Select(choices=Cita.ASUNTOS),
            'semestre': forms.Select(choices=Cita.SEMESTRES),
        }   

class FormularioHorario(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['inicio', 'fin', 'estado']
        
