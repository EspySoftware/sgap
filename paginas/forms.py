from django.forms import ModelForm
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
