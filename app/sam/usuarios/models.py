from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

#CLASE USUARIO GENERAL

class Alumno(models.Model):
  TYPE_CARRERA = [
        ('INF', 'Ejecución'),
        ('ICI', 'Civil'),
    ]
  nombre = models.CharField(max_length = 255, null=False)
  apellidos = models.CharField(max_length = 255, null=False)
  rut = models.CharField(max_length = 50, unique=True, null=False)
  generacion = models.IntegerField(default=2019)
  email = models.EmailField(max_length=254, unique=True, null=False, default='')
  emailPersonal = models.EmailField(default=None, max_length=254)
  es_Mechon = models.BooleanField(default=True, null=False)
  carrera = models.CharField(max_length=10, choices=TYPE_CARRERA, null=False, default='')

  usuario = models.OneToOneField(User, on_delete = models.CASCADE)



  def __str__(self):
    return u"%s %s" % (self.nombre, self.apellidos)
