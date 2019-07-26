from django.contrib import admin
from .models import Encuesta
from .models import Pregunta
from .models import Alternativa

# Register your models here.

admin.site.register(Encuesta)
admin.site.register(Pregunta)
admin.site.register(Alternativa)