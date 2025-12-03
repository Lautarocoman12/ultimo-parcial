from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar, name='buscar'),
    path('email/', views.enviar_resultados, name='enviar_resultados'),
]
