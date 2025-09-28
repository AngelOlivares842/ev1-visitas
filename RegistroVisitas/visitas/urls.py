from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_visita, name='registrar_visita'),
    path('listado/', views.listado_visitas, name='listado_visitas'),
    path('salida/<int:visita_id>/', views.registrar_salida, name='registrar_salida'),
    path('dashboard/', views.dashboard_visitas, name='dashboard_visitas'),
]