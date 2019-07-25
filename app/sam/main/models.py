from django.db import models
from usuarios.models import Padrino

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


class Grupo(models.Model):
  numero = models.IntegerField(default=0)
  padrino = models.ForeignKey(Padrino, on_delete = models.CASCADE)

