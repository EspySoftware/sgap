from django.forms import ModelForm
from .models import Cita

class FormularioCita(ModelForm):
    class Meta:
        model = Cita
        fields = ['titulo', 'motivo', 'fecha']