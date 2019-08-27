from django.db import models
from datetime import date, datetime

# Create your models here.
#CLASE ENCUESTA

class Encuesta(models.Model):
  description = models.CharField(max_length = 255)
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
      return self.description

class Pregunta(models.Model):
  description = models.CharField(max_length = 255)
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
      return self.description

class Alternativa(models.Model):
  description = models.CharField(max_length = 255)
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
      return self.description

class EncuestaPregunta(models.Model):
  encuesta = models.ForeignKey(Encuesta, on_delete = models.PROTECT)
  pregunta = models.ForeignKey(Pregunta, on_delete = models.PROTECT)
  order = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
      return 'Encuesta={0}, Pregunta={1}, Posicion={2}'.format(self.encuesta, self.pregunta,self.order)


class PreguntaAlternativa(models.Model):
    pregunta = models.ForeignKey(Pregunta,on_delete= models.PROTECT)
    alternativa = models.ForeignKey(Alternativa,on_delete = models.PROTECT)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return 'Pregunta={0}, Alternativa={1}, Posicion={2}'.format(self.pregunta, self.alternativa,self.order)