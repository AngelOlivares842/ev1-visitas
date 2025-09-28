from django import forms
from .models import Visita

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['nombre', 'rut', 'motivo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese nombre completo'
            }),
            'rut': forms.TextInput(attrs={
                'placeholder': 'Ej: 12345678-9'
            }),
            'motivo': forms.Select(attrs={})
        }
    
    def clean_rut(self):
        rut = self.cleaned_data['rut']
        visita = Visita()
        
        # Usar estructura de decisión para validar
        if not visita.validar_rut(rut):
            raise forms.ValidationError('RUT inválido. Formato: 12345678-9')
        
        return rut
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        
        # Validar que el nombre solo contenga letras y espacios
        if not all(c.isalpha() or c.isspace() for c in nombre):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios')
        
        # Validar longitud mínima
        if len(nombre.strip()) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
        
        return nombre.strip()