from django.forms import ModelForm
from .models import Cita
from django import forms

class FormularioCita(ModelForm):
    class Meta:
        model = Cita
        fields = ['titulo', 'motivo', 'fecha', 'estado']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea,
        }

