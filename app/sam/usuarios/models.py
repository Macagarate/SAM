from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from encuesta.models import Encuesta

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
    return 'Rut={0}, Nombre={1}, Apellidos={2}, Generacion={3}, Carrera={4}'.format(self.rut, self.nombre,self.apellidos,self.generacion,self.carrera)

class Actividad(models.Model):
  alumno = models.ForeignKey(Alumno, on_delete = models.PROTECT)
  anno_participacion = models.IntegerField(default=0)
  rol = models.IntegerField(default=0)
  status = models.BooleanField(default=False)  #status 0|1 
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return 'Alumno=({0}), Año Participacion={1}, Rol={2}'.format(self.alumno, self.anno_participacion,self.rol)
