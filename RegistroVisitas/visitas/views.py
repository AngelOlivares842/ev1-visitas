from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from .models import Visita
from .forms import VisitaForm
from datetime import datetime, date

def registrar_visita(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_visitas')
    else:
        form = VisitaForm()
    
    return render(request, 'visitas/registrar.html', {'form': form})

def listado_visitas(request):
    hoy = date.today()
    visitas_hoy = Visita.objects.filter(fecha=hoy).order_by('-hora_entrada')
    
    # Usar estructura de decisión para categorizar visitas
    visitas_activas = []
    visitas_finalizadas = []
    
    for visita in visitas_hoy:
        if visita.en_visita:
            visitas_activas.append(visita)
        else:
            visitas_finalizadas.append(visita)
    
    context = {
        'visitas_activas': visitas_activas,
        'visitas_finalizadas': visitas_finalizadas,
        'total_visitas': len(visitas_activas) + len(visitas_finalizadas),
        'hoy': hoy.strftime('%d/%m/%Y')
    }
    
    return render(request, 'visitas/listado.html', context)

def registrar_salida(request, visita_id):
    try:
        visita = get_object_or_404(Visita, id=visita_id)
        
        # Verificar si ya tiene hora de salida
        if visita.hora_salida is None:
            visita.hora_salida = timezone.now()
            visita.save()
            messages.success(request, f'Salida registrada correctamente para {visita.nombre}')
        else:
            messages.warning(request, f'{visita.nombre} ya tenía hora de salida registrada')
            
    except Exception as e:
        messages.error(request, f'Error al registrar salida: {str(e)}')
    
    return redirect('listado_visitas')

def dashboard_visitas(request):
    hoy = date.today()
    visitas_hoy = Visita.objects.filter(fecha=hoy)
    
    # Estadísticas usando estructuras de decisión
    estadisticas = {
        'total': visitas_hoy.count(),
        'activas': visitas_hoy.filter(hora_salida__isnull=True).count(),
        'finalizadas': visitas_hoy.filter(hora_salida__isnull=False).count(),
    }
    
    # Conteo por motivo
    conteo_motivos = {}
    for motivo in Visita.MOTIVOS_VISITA:
        conteo = visitas_hoy.filter(motivo=motivo[0]).count()
        conteo_motivos[motivo[1]] = conteo
    
    context = {
        'estadisticas': estadisticas,
        'conteo_motivos': conteo_motivos,
        'hoy': hoy
    }
    
    return render(request, 'visitas/dashboard.html', context)