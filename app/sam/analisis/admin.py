from django.contrib import admin
from .models import Grupo, Respuesta, Afinacion, Resultado

# Register your models here.

admin.site.register(Grupo)
admin.site.register(Respuesta)
admin.site.register(Afinacion)
admin.site.register(Resultado)

