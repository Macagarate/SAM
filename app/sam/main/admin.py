from django.contrib import admin
from .models import Encuesta, Pregunta, Respuesta, Afinacion, Resultado


# Register your models here.


admin.site.register(Respuesta)


admin.site.register(Afinacion)
admin.site.register(Resultado)