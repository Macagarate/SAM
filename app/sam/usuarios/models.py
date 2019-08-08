from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

#CLASE USUARIO GENERAL

class Alumno(models.Model):
  nombre = models.CharField(max_length = 255)
  apellidos = models.CharField(max_length = 255)
  rut = models.CharField(max_length = 50, unique=True)
  generacion = models.IntegerField(default=2019)
  email = models.EmailField(default=None, max_length=254, unique=True)
  emailPersonal = models.EmailField(default=None, max_length=254)
  es_Mechon=models.BooleanField(default=None)
  usuario = models.OneToOneField(User, on_delete = models.CASCADE)
  #FALTA CARRERA


  def __str__(self):
    return u"%s %s" % (self.nombre, self.apellidos)
