from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('login/', auth_views.LoginView.as_view(), name="login"),
   path('logout/', auth_views.LogoutView.as_view(), name="logout"),
   path('home/', views.index, name="home"),
   
   # Parte de encuestas
   path('encuesta/', views.encuesta, name="encuesta"),
   path('encuestas/', views.encuestas, name="encuestas"),
   path('encuestas/crear_encuesta', views.crearEncuesta, name="crearEncuesta"),
   path('encuestas/ver_encuesta/<int:encuesta_id>', views.verEncuesta, name="verEncuesta"),
   path('encuestas/editar_encuesta', views.editarEncuesta, name="editarEncuesta"),
   path('encuestas/update_encuesta', views.updateEncuesta, name="updateEncuesta"),
   path('encuestas/eliminar_encuesta', views.eliminarEncuesta, name="eliminarEncuesta"),
   
   #Menu Principal
   path('perfil/', views.perfil, name="perfil"),
   path('resultado/', views.resultadoEncuesta, name="resultadoEncuesta"),
   path('resultados/', views.resultadosEncuestas, name="resultadosEncuestas"),
   path('mechones/', views.listadoMechones, name="mechones"),
   path('padrinos/', views.listadoPadrinos, name="padrinos"),
   path('grupos/', views.grupos, name="grupos"),
   path('grupo/', views.grupo, name="grupo"),

   #Matchmaking
   path('enviar_encuesta/', views.enviarEncuesta, name="enviar_encuesta"),
   path('import_users/', views.import_users, name="import_users"),

   #Usuarios
   path('crear-usuario/', views.nuevoAlumno, name="crear-usuario"),
   path('crear-alumno/', views.crear_alumno, name="crear-alumno"),
   


]