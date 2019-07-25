from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from analisis.models import Grupo


# Create your models here.


#CLASE USUARIO GENERAL

class Usuario(models.Model):
  nombre = models.CharField(max_length = 255)
  apellidos = models.CharField(max_length = 255)
  rut = models.CharField(max_length = 255)
  generacion = models.IntegerField(default=2019)
  email = models.EmailField(default=None, max_length=254, unique=True)
  emailPersonal = models.EmailField(default=None, max_length=254)
  usuario = models.ForeignKey(User, on_delete = models.CASCADE)

  def __str__(self):
    return u"%s %s" % (self.nombre, self.apellidos)

    # HERENCIA DE USUARIO; PADRINO

class Padrino(Usuario):
  calificacion = models.IntegerField(default=0)

  def __str__(self):
    return self.calificacion


# HERENCIA DE USUARIO; MECHON. NO SE DEBERIA BORRAR SI NO PERTENECE A UN GRUPO

class Mechon(Usuario):
  calificacion = models.IntegerField(default=0)
  grupo = models.ForeignKey(
    Grupo, 
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
  ) 
  def __str__(self):
    return self.calificacion
