from django.db import models
from django.contrib.auth.models import User

class Alumno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    nota = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
