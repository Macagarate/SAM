from django.contrib import admin
from .models import Alumno
from .models import Actividad

# Register your models here.

admin.site.register(Alumno)
admin.site.register(Actividad)

