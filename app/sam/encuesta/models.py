from django.db import models
from datetime import date, datetime

# Create your models here.
#CLASE ENCUESTA

class Encuesta(models.Model):
  anno = models.DateField(default=date.today)
  activado = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def get_year(self):
    return self.anno.year

#CLASE PREGUNTA ASOCIADA A UNA ENCUESTA

class Pregunta(models.Model):
  texto = models.TextField()
  tipoObligatoria = models.BooleanField(default=True)
  encuesta = models.ForeignKey(Encuesta, on_delete = models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.texto

class Alternativa(models.Model):
  texto = models.TextField()
  pregunta = models.ForeignKey(Pregunta, related_name='alternativa_pregunta',on_delete = models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.texto
  