from django.forms import ModelForm
from .models import Cita, Horario
from django import forms
from .models import Cita
from django.utils import timezone

class StringModelChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        # Get the original value (a Horario object)
        original_value = super().to_python(value)
        # Convert the 'inicio' attribute to a string in ISO 8601 format
        return original_value.inicio.isoformat() if original_value else ''

class FormularioCita(ModelForm):
    fecha = StringModelChoiceField(
        queryset=Horario.objects.none(),  # Inicialmente vacío
        to_field_name='inicio',
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['fecha'].queryset = Horario.objects.filter(estado="disponible", inicio__gt=timezone.now())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user.is_staff:
            self.fields['fecha'].queryset = Horario.objects.filter(estado="disponible")
        else:
            self.fields['fecha'].queryset = Horario.objects.filter(estado="disponible", inicio__gt=timezone.now())

    class Meta:
        model = Cita
        fields = ['matricula', 'apellido_paterno', 'apellido_materno', 'nombre', 'sexo', 'semestre', 'carrera',
                  'asunto', 'descripcion', 'fecha', 'estado', 'comentarios_orientador', 'comentarios_usuario']
        widgets = {
            'descripcion': forms.Textarea,
            'sexo': forms.Select(choices=Cita.GENERO),
            'carrera': forms.Select(choices=Cita.CARRERAS),
            'asunto': forms.Select(choices=Cita.ASUNTOS),
            'semestre': forms.Select(choices=Cita.SEMESTRES),
            'fecha': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
        }


class FormularioHorario(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['inicio', 'fin', 'estado']
