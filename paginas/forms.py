from django.forms import ModelForm
from .models import Cita, Horario
from django import forms
from .models import Cita

# Este hack hace que el campo 'fecha' del formulario funcione y pueda convertir el objeto Horario a un string en formato ISO 8601
# La verdad no sé cómo funciona pero funciona
class StringModelChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        # Get the original value (a Horario object)
        original_value = super().to_python(value)
        # Convert the 'inicio' attribute to a string in ISO 8601 format
        return original_value.inicio.isoformat() if original_value else ''

class FormularioCita(ModelForm):
    fecha = StringModelChoiceField(
        queryset=Horario.objects.filter(estado="disponible"),
        to_field_name='inicio',
    )

    class Meta:
        model = Cita
        fields = ['matricula', 'apellido_paterno', 'apellido_materno', 'nombre', 'sexo', 'semestre', 'carrera', 'asunto', 'descripcion', 'fecha', 'estado', 'comentarios_orientador', 'comentarios_usuario']
        widgets = {
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
        
