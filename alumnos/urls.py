from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('crear/', views.crear_alumno, name='crear_alumno'),
    path('pdf/<int:id>/', views.generar_pdf, name='generar_pdf'),
    path('csv/', views.exportar_csv, name='exportar_csv'),
]
