from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar, name='scraper'),
    path('enviar/', views.enviar_resultados, name='enviar_resultados'),
]
