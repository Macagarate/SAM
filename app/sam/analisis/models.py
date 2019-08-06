from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from encuesta.models import Alternativa
from usuarios.models import Apadrinamiento


#CLASE RESULTADO QUE CONTIENE FOREIGN KEYS AL ALUMNO Y A LA ENCUESTA CORRESPONDIENTE

class RespuestaEncuesta(models.Model):
  participante = models.ForeignKey(Apadrinamiento, on_delete = models.PROTECT)
  alternativa = models.ForeignKey(Alternativa, on_delete = models.PROTECT)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)