from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from encuesta.models import Encuesta

#CLASE USUARIO GENERAL

class Alumno(models.Model):
  nombre = models.CharField(max_length = 255)
  apellidos = models.CharField(max_length = 255)
  rut = models.CharField(max_length = 50, unique=True)
  generacion = models.IntegerField(default=2019)
  email = models.EmailField(default=None, max_length=254, unique=True)
  emailPersonal = models.EmailField(default=None, max_length=254)
  es_Mechon = models.BooleanField(default=None)
  carrera = models.CharField(max_length = 255)
  usuario = models.OneToOneField(User, on_delete = models.CASCADE)

  def __str__(self):
    return u"%s %s" % (self.nombre, self.apellidos)

class Actividad(models.Model):
  alumno = models.ForeignKey(Alumno, on_delete = models.PROTECT)
  anno_participacion = models.IntegerField(default=0)
  rol = models.IntegerField(default=0)
  status = models.BooleanField(default=False)  #status 0|1 
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  #ref_encuesta = models.ForeignKey(Encuesta, on_delete = models.PROTECT)
  
  #ref_pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE)
  #ref_respuesta = models.ForeignKey(Respuesta, on_delete = models.CASCADE)
  #ref_preguntas = models.ManyToManyField(Pregunta)
  #ref_respuestas = models.ManyToManyField(Respuesta)

  def __str__(self):
    return 
