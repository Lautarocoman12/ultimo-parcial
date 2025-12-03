from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Alumno
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import csv

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password)

        # Enviar email de bienvenida
        send_mail(
            "Bienvenido",
            "Gracias por registrarte!",
            None,
            [email],
            fail_silently=True
        )

        return redirect('login')
    return render(request, 'registro.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'alumnos': alumnos})


@login_required
def crear_alumno(request):
    if request.method == 'POST':
        Alumno.objects.create(
            user=request.user,
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            nota=request.POST['nota']
        )
        return redirect('dashboard')
    return render(request, 'crear.html')


@login_required
def generar_pdf(request, id):
    alumno = Alumno.objects.get(id=id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="alumno_{alumno.id}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, f"Alumno: {alumno.nombre} {alumno.apellido}")
    p.drawString(100, 730, f"Nota: {alumno.nota}")
    p.showPage()
    p.save()

    # Envío por email (si falla, no rompe)
    try:
        send_mail(
            "PDF Alumno",
            "Adjunto PDF",
            None,
            [request.user.email],
            fail_silently=True
        )
    except:
        pass

    return response


@login_required
def exportar_csv(request):
    alumnos = Alumno.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumnos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Apellido', 'Nota'])

    for alumno in alumnos:
        writer.writerow([alumno.nombre, alumno.apellido, alumno.nota])

    return response
