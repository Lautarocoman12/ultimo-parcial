from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

@login_required
def buscar(request):
    resultados = []
    if request.method == 'POST':
        palabra = request.POST['palabra']
        url = f"https://es.wikipedia.org/wiki/{palabra}"
        headers = {"User-Agent": "Mozilla/5.0"}  
        r = requests.get(url, headers=headers)   

        soup = BeautifulSoup(r.text, 'html.parser')

        primeros = soup.find_all('p', limit=3)
        resultados = [p.text for p in primeros]

    return render(request, 'scraper.html', {'resultados': resultados})


@login_required
def enviar_resultados(request):
    resultados = request.POST.getlist('resultados')

    mensaje = "\n\n".join(resultados)
    send_mail(
        "Resultados Scraping",
        mensaje,
        None,  # remitente (puede ser tu EMAIL_HOST_USER si querés)
        [request.user.email],
        fail_silently=True
    )

    return render(request, 'scraper.html', {'resultados': resultados, 'ok': True})
