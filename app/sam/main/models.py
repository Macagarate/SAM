from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

#CLASE ENCUESTA

class Encuesta(models.Model):
  anno = models.DateField(default=date.today)
  activado = models.BooleanField(default=False)
  
  def get_year(self):
    return self.anno.year


#CLASE PREGUNTA ASOCIADA A UNA ENCUESTA

class Pregunta(models.Model):
  texto = models.TextField()
  tipoObligatoria = models.BooleanField(default=True)
  encuesta = models.ForeignKey(Encuesta, on_delete = models.CASCADE)

  def __str__(self):
    return self.texto
  



#CLASE RESPUESTA ASOCIADA A UNA PREGUNTA

class Respuesta(models.Model):
  texto = models.TextField()
  #Acá van las variables del test
  #....
  #....
  pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE)

  def __str__(self):
    return self.texto



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



#CLASE GRUPO, FOREIGN KEY A PADRINO

class Grupo(models.Model):
  numero = models.IntegerField(default=0)
  padrino = models.ForeignKey(Padrino, on_delete = models.CASCADE)



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



