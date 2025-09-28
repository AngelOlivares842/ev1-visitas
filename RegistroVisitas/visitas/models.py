from django.db import models
from django.core.exceptions import ValidationError
import re
from datetime import date, timezone

class Visita(models.Model):
    MOTIVOS_VISITA = [
        ('reunion', 'Reunión de Trabajo'),
        ('entrega', 'Entrega de Documentos'),
        ('mantenimiento', 'Mantenimiento'),
        ('visita', 'Visita Personal'),
        ('otro', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    motivo = models.CharField(max_length=20, choices=MOTIVOS_VISITA)
    hora_entrada = models.DateTimeField(auto_now_add=True)
    hora_salida = models.DateTimeField(null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    
    def clean(self):
        # Validar RUT usando estructuras de decisión
        if not self.validar_rut(self.rut):
            raise ValidationError({'rut': 'RUT inválido'})
        
        # Validar que la hora de salida sea posterior a la de entrada
        if self.hora_salida and self.hora_salida <= self.hora_entrada:
            raise ValidationError({'hora_salida': 'La hora de salida debe ser posterior a la hora de entrada'})
    
    def validar_rut(self, rut):
        """Valida el formato y dígito verificador del RUT"""
        try:
            rut = rut.upper().replace('.', '').replace('-', '')
            cuerpo = rut[:-1]
            dv = rut[-1]
            
            # Validar formato usando estructura de decisión
            if not cuerpo.isdigit() or (dv not in '0123456789K'):
                return False
            
            # Calcular dígito verificador
            suma = 0
            multiplo = 2
            
            for digito in reversed(cuerpo):
                suma += int(digito) * multiplo
                multiplo += 1
                if multiplo == 8:
                    multiplo = 2
            
            resto = suma % 11
            dv_calculado = 11 - resto
            
            if dv_calculado == 10:
                dv_calculado = 'K'
            elif dv_calculado == 11:
                dv_calculado = '0'
            else:
                dv_calculado = str(dv_calculado)
            
            return dv == dv_calculado
            
        except:
            return False
    
    def registrar_salida(self):
        self.hora_salida = timezone.now()
        self.save()
    
    @property
    def en_visita(self):
        return self.hora_salida is None
    
    def __str__(self):
        return f"{self.nombre} - {self.rut}"

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'