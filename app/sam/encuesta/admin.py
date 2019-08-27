from django.contrib import admin
from .models import Encuesta
from .models import Pregunta
from .models import Alternativa
from .models import EncuestaPregunta
from .models import PreguntaAlternativa

# Register your models here.

admin.site.register(Encuesta)
admin.site.register(Pregunta)
admin.site.register(Alternativa)
admin.site.register(EncuestaPregunta)
admin.site.register(PreguntaAlternativa)

    