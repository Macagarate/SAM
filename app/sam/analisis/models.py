from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from encuesta.models import Encuesta
from encuesta.models import Pregunta
from usuarios.models import Usuario
from usuarios.models import Padrino
from usuarios.models import Mechon



# Create your models here.



#CLASE GRUPO, FOREIGN KEY A PADRINO

class Grupo(models.Model):
  numero = models.IntegerField(default=0)
  padrino = models.ForeignKey(Padrino, on_delete = models.CASCADE)



#CLASE AFINACION ENTRE PADRINO Y MECHON

class Afinacion(models.Model):
  afinidad = models.FloatField(default=0)
  padrino = models.ForeignKey(Padrino, on_delete = models.CASCADE)
  mechon = models.ForeignKey(Mechon, on_delete = models.CASCADE)

  def __str__(self):
    return self.afinidad


#CLASE RESULTADO QUE CONTIENE FOREIGN KEYS AL ALUMNO Y A LA ENCUESTA CORRESPONDIENTE

class Resultado(models.Model):
  #Faltan saber las variables de la Encuesta
  #....
  #....
  alumno = models.ForeignKey(Usuario, on_delete = models.CASCADE)
  encuesta = models.ForeignKey(Encuesta, on_delete = models.CASCADE)
  fecha_realizacion = models.DateTimeField(default=datetime.now)

  def __str__(self):
    return self.fecha_realizacion