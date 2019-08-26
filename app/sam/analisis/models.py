from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from encuesta.models import Alternativa
from encuesta.models import Pregunta
from encuesta.models import Encuesta
from usuarios.models import Alumno



# Create your models here.



#CLASE GRUPO, FOREIGN KEY A PADRINO

class Grupo(models.Model):
  numero = models.IntegerField(default=0)
  padrino = models.ForeignKey(Alumno, on_delete = models.CASCADE)



#CLASE AFINACION ENTRE PADRINO Y MECHON

class Afinacion(models.Model):
  afinidad = models.FloatField(default=0)
  padrino = models.ForeignKey(Alumno, on_delete = models.CASCADE, related_name = 'padrino_set')
  mechon = models.ForeignKey(Alumno, on_delete = models.CASCADE, related_name = 'mechon_set')

  def __str__(self):
    return self.afinidad


#CLASE RESULTADO QUE CONTIENE FOREIGN KEYS AL ALUMNO Y A LA ENCUESTA CORRESPONDIENTE

class Respuesta(models.Model):
  alumno = models.ForeignKey(Alumno, on_delete = models.CASCADE)
  encuesta_alumno = models.ForeignKey(Encuesta, on_delete = models.CASCADE)
  pregunta_encuesta = models.ForeignKey(Pregunta, on_delete = models.CASCADE)
  alternativa_alumno = models.ForeignKey(Alternativa, on_delete = models.CASCADE)
  fecha_realizacion = models.DateTimeField(default=datetime.now)

  def __str__(self):
    return self.fecha_realizacion


# Contiene las referencias de Alumnos y Encuesta, y se utilizará para la generación 
# del ranking para cada alumno (padrino o mechon) los cuales no se referencian, se registran inmediatamente.

class Respuesta(models.Model):
    respuesta = models.IntegerField(default=0,max_length = 5)

class Actividad(models.Model):
  anno_participacion = models.IntegerField(default=0)
  rol = models.IntegerField(default=0)
  status = models.BooleanField(default=False)  #status 0|1 
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  ref_encuesta = models.ForeignKey(Encuesta, on_delete = models.CASCADE)
  ref_alumno = models.ForeignKey(Alumno, on_delete = models.CASCADE)
  #ref_pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE)
  #ref_respuesta = models.ForeignKey(Respuesta, on_delete = models.CASCADE)
  ref_preguntas = models.ManyToManyField(Pregunta)
  ref_respuestas = models.ManyToManyField(Respuesta)

  

