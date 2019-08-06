from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

#CLASE USUARIO GENERAL

class Usuario(models.Model):
  rut = models.CharField(max_length = 255)
  nombre = models.CharField(max_length = 255)
  apellidos = models.CharField(max_length = 255)
  generacion = models.IntegerField(default=2019)
  email = models.EmailField(default=None, max_length=254, unique=True)
  emailPersonal = models.EmailField(default=None, max_length=254)
  usuario = models.OneToOneField(User, on_delete = models.CASCADE)

  def __str__(self):
    return u"%s %s" % (self.nombre, self.apellidos)

    # HERENCIA DE USUARIO; PADRINO

  def isMechon(self):
    return self.generacion==date.year

  def tipoUsuario(self):
    if(self.isMechon(self)):
      return "MECHON"
    return "PADRINO"


class Apadrinamiento(models.Model):
  PROCESS_STATUS = [
        ('PR', 'Mechon'),
        ('AH', 'Ahijado'),
    ]
  anioParticipacion = models.IntegerField(default=2019)
  estadoProceso = models.CharField(max_length=2, choices= PROCESS_STATUS)
  usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "" 