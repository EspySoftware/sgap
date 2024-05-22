from django.forms import ModelForm
<<<<<<< Updated upstream
=======
from .models import Cita, Horario
>>>>>>> Stashed changes
from django import forms
from .models import Cita

class FormularioCita(ModelForm):
    class Meta:
        model = Cita
        fields = ['titulo', 'motivo', 'fecha', 'estado']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea,
        }

class FormularioHorario(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['inicio', 'fin', 'estado']
        
