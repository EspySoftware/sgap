from django.forms import ModelForm
from .models import Cita, Horario
from django import forms
from .models import Cita

class FormularioCita(ModelForm):
    class Meta:
        model = Cita
        fields = ['matricula', 'ap_paterno', 'ap_materno', 'nombre', 'sexo', 'semestre', 'carrera', 'asunto', 'descripcion', 'fecha', 'estado', 'comentarios']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea,
            'sexo': forms.Select(choices=Cita.GENERO),
            'carrera': forms.Select(choices=Cita.CARRERAS),
            'asunto': forms.Select(choices=Cita.ASUNTOS),
        }   

class FormularioHorario(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['inicio', 'fin', 'estado']
        
