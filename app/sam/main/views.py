import csv, io  
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from usuarios.models import Alumno, Actividad
from analisis.models import Grupo
from encuesta.models import Encuesta, Pregunta, Alternativa, EncuestaPregunta, PreguntaAlternativa
from analisis.models import Respuesta, Afinacion, Grupo
import datetime
from datetime import date, datetime
import logging
from django.urls import reverse
from django.template import *



#-------------------------------------------------------------FUNCIONES GENERALES!


##############---------FUNCIONES HANDLERS ERRORES 404 500----------####################

def handler404(request):
    return render(request, '404.html', status=404)
    
def handler500(request):
    return render(request, '500.html', status=500)



def crearUser(request, nombre=None, apellido=None, email=None): #Creacion de nuevos usuarios
    
    
    a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN' #Evitar problemas letras especiales y tildes
    trans = str.maketrans(a,b)
    nombre_nuevo = nombre.translate(trans)
    apellido_nuevo = apellido.translate(trans)

    first_letra = nombre_nuevo[:1].lower()
    apellidoSplit = apellido_nuevo.split(" ")
    first_apellido = apellidoSplit[0].lower()
    second_apellido = apellidoSplit[1][:1].lower()
    
    primerNombre = nombre_nuevo.split(" ")[0]
    primerApellido =apellidoSplit[0]

    userName = first_letra + first_apellido + second_apellido
    userExiste = User.objects.filter(username=userName)
    if not userExiste:
        userPass = userName + '99'
        userEmail = email

        user = User.objects.create_user(username=userName,
                                        email=userEmail,
                                        password=userPass,
                                        first_name=primerNombre,
                                        last_name=primerApellido)
        user.save()
        del user
        return True

    return False





##############---------FUNCION ENVIO ENCUESTA----------###################

@login_required()
def enviarEncuesta(request):
    template = "encuesta.html"

    if request.method == 'GET':
        return render(request, template)

    if request.method == 'POST':
        try:
            now = date.today().year
            encuesta = Encuesta.objects.get(activado=True)
            alumno = Alumno.objects.get(usuario=request.user.id)
            preguntas = EncuestaPregunta.objects.filter(encuesta = encuesta.id)
            actividad = Actividad.objects.get(alumno=alumno, anno_participacion=now)

            for p in preguntas:
                respuesta = Respuesta()
                respuesta.encuesta = encuesta
                respuesta.pregunta = p.pregunta
                respuesta.alternativa = Alternativa.objects.get(id=request.POST.get(str(p.pregunta.id)))
                respuesta.actividad = actividad
                respuesta.save()
            
            actividad.status = True
            actividad.save()
            messages.success(request, '¡Encuesta contestada exitosamente!')
            return HttpResponseRedirect(reverse("resultadoEncuesta"))
        
        except Exception as e:
            messages.error(request,"No fue posible enviar encuesta. "+repr(e))
            return HttpResponseRedirect(reverse("encuesta"))


    return render(request, 'home.html')





##############---------FUNCIONES DE RENDER----------####################


@login_required()
def index(request): #Home
    return render(request, 'home.html')


@login_required()
def encuesta(request): #Para realizar encuesta
    now = date.today().year
    encuesta = Encuesta.objects.get(activado=True)
    alumno = Alumno.objects.get(usuario=request.user.id)
    actividad = Actividad.objects.get(alumno=alumno, anno_participacion=now)
    respuesta = Respuesta.objects.filter(actividad=actividad)
        
    if not respuesta:
        preguntas = EncuestaPregunta.objects.filter(encuesta = encuesta.id)
        alternativas = PreguntaAlternativa.objects.all()
        del actividad
        del alumno
        messages.info(request, 'Sólo se puede responder una vez, responda con conciencia.')
        return render(request, 'encuesta.html', {'preguntas': preguntas, 'alternativas': alternativas})

    del encuesta
    del alumno
    del actividad
    messages.warning(request, 'Usted ya respondió la encuesta')
    return render(request, 'encuesta.html')
    
    
            

@login_required()
def perfil(request): #Vista perfil usuario
    perfil = Alumno.objects.get(usuario=request.user.id)
    return render(request, 'perfil.html', {'perfil': perfil})


@login_required()
def resultadoEncuesta(request): #Vista resultado alumno
    return render(request, 'resultado-encuesta.html')


@login_required()
def grupo(request): #Vista grupo alumno
    perfil = Alumno.objects.get(usuario=request.user.id)
    grupos = Grupo.objects.all()
    if perfil.es_Mechon == True:
        grupo_a = Grupo.objects.filter(ahijado=perfil)
        padrino = grupo_a[0].padrino
        grupo_p = Grupo.objects.filter(padrino=padrino)
        grupo = grupo_a | grupo_p
        print (grupo)
        print (grupo[0])
    else:
        grupo = Grupo.objects.filter(padrino=perfil)
    return render(request, 'grupo.html', {'perfil':perfil, 'grupos': grupos, 'grupo': grupo})






##############---------FUNCION DE CAMBIO PASSWORD----------####################


@login_required()
def cambiar_pass(request):
    template = "cambiar_pass.html"

    if request.method == 'GET':
        return render(request, template)

    if request.method == 'POST':
        try:
            passVieja = request.POST.get('inputPassVieja')
            passNueva = request.POST.get('inputPassNueva')
            passConfirmacion = request.POST.get('inputPassConfirmada')

            user = authenticate(username=request.user.username, password=passVieja)

            if user is not None:
                if passNueva == passConfirmacion:
                    user.set_password(passNueva)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, '¡Contraseña cambiada con éxito!')
                else:
                    messages.error(request,'Las contraseñas no coinciden')
                    return HttpResponseRedirect(reverse("cambiar_pass"))
            else:
                messages.error(request,'La contraseña no es la correcta')
                return HttpResponseRedirect(reverse("cambiar_pass"))
            
        except Exception as e:
            messages.error(request,"No es posible cambiar contraseña. "+repr(e))
            return HttpResponseRedirect(reverse("cambiar_pass"))

        return HttpResponseRedirect(reverse("cambiar_pass"))
    
    #return render(request, 'cambiar_pass.html')








#----------------------------------------------------------FUNCIONES SÓLO ADMIN!


##############---------FUNCIONES LISTADO----------###################

@staff_member_required()
def listadoMechones(request): #Vista de todos los ahijados
    mechones = Alumno.objects.filter(es_Mechon=True)
    return render(request, 'listadoMechones.html', {'mechones': mechones})



@staff_member_required()
def listadoPadrinos(request): #Vista de todos los padrinos
    padrinos = Alumno.objects.filter(es_Mechon=False)
    return render(request, 'listadoPadrinos.html', {'padrinos': padrinos})



@staff_member_required()
def grupos(request): #Vista de todos los grupos creados
    now = date.today().year
    grupos = Grupo.objects.all()
    actividades = Actividad.objects.filter(anno_participacion=now, rol=1)
    print(grupos)
    return render(request, 'grupos.html', {'grupos': grupos, 'actividades': actividades})





##############---------FUNCIONES ENCUESTA----------###################


@staff_member_required()
def resultadosEncuestas(request): #Vista de todos los resultados de los alumnos
    actividades = Actividad.objects.all()
    respuestas = Respuesta.objects.all()
    return render(request, 'resultados-encuestas.html', {'actividades': actividades, 'respuestas': respuestas})


@staff_member_required()
def encuestas(request): #Vista de todas las encuestas
    encuestas = Encuesta.objects.all()
    preguntas = EncuestaPregunta.objects.all()
    alternativas = PreguntaAlternativa.objects.all()
    return render(request, 'encuestas.html', {'encuestas': encuestas, 'preguntas': preguntas, 'alternativas': alternativas})

@staff_member_required()
def crearEncuesta(request): #Crear encuesta nueva (NO TERMINADA)
    template = "crear_encuesta.html"

    if request.method == 'GET':
        return render(request, template)
    
    if request.method == 'POST':
        try:
            encuesta = Encuesta()
            anno = request.POST.get('inputAnno')
            encuesta.anno = datetime.date(int(anno),1,1)
            activado = request.POST.get('inputActivo')
            
            if activado == '1':
                encuesta.activado = True
                for i in Encuesta.objects.all():
                    i.activado = False
                    i.save()

            encuesta.save()
            messages.success(request, '¡Encuesta agregada con éxito!')
            del encuesta

        except Exception as e:
            messages.error(request,"No fue posible crear encuesta. "+repr(e))
            del encuesta
            return HttpResponseRedirect(reverse("crearEncuesta"))
            
        return HttpResponseRedirect(reverse("crearEncuesta"))


@staff_member_required()
def updateEncuesta(request): #Actualizar una encuesta (NO HECHA)
    return redirect()

@staff_member_required()
def eliminarEncuesta(request): #Eliminar una encuesta (NO HECHA)
    return redirect()






##############---------FUNCIONES USUARIOS----------###################

@staff_member_required()
def crear_alumno(request): #Crear alumno, usuario y actividad nuevo
    template = "crear_usuario.html"

    if request.method == 'GET':
        return render(request, template)
    
    if request.method == 'POST':
        try:
            
            alumno = Alumno()
            nombre_alumno = request.POST.get('inputNombre')
            apellidos_alumno = request.POST.get('inputApellido')
            email_alumno = request.POST.get('inputEmail1')
            txt_rut =  request.POST.get('inputRut')
            rut = txt_rut.replace(".", "")
            alumnoExiste = Alumno.objects.filter(rut=rut)
            
            if not alumnoExiste:

                apellidos = apellidos_alumno.split(" ")

                if len(apellidos) == 1:
                    messages.error(request,'Ingrese al menos dos apellidos')
                    del alumno
                    return HttpResponseRedirect(reverse("crear_alumno"))
                
                emailSplit = email_alumno.split("@")

                if emailSplit[1] != "mail.pucv.cl":
                    messages.error(request,'Ingrese mail institucional válido')
                    del alumno
                    return HttpResponseRedirect(reverse("crear_alumno"))

                alumno.nombre = nombre_alumno.upper()
                alumno.apellidos = apellidos_alumno.upper()
                alumno.rut = rut
                alumno.generacion = request.POST.get('inputGeneracion')
                alumno.email = email_alumno
                alumno.emailPersonal = request.POST.get('inputEmail2')
                alumno.carrera = request.POST.get('inputCarrera')
                
                if request.POST.get('inputTipo') == 'PADRINO':
                    alumno.es_Mechon =  False
                
                else:
                    alumno.es_Mechon =  True
                    
                if crearUser('post', nombre_alumno, apellidos_alumno, email_alumno):
                    usuario_alumno = User.objects.filter(email=email_alumno)
                    alumno.usuario = usuario_alumno[0]
                    alumno.save()
                    now = date.today().year
                    actividad = Actividad()
                    actividad.alumno = Alumno.objects.get(rut=rut)
                    actividad.status = False
                    actividad.anno_participacion = now
                    if request.POST.get('inputGeneracion') == now:
                        actividad.rol = 0        
                    else:
                        actividad.rol = 1
                    actividad.save()
                    messages.success(request, '¡Alumno agregado con éxito!')
                    del alumno
                else:
                    messages.error(request,'ERROR - Alumno no pudo ser creado')
                    del alumno
                    return HttpResponseRedirect(reverse("crear_alumno"))
            else:
                messages.error(request,'¡Este usuario ya existe!')
                del alumno
                return HttpResponseRedirect(reverse("crear_alumno"))
        
        except Exception as e:
            messages.error(request,"No fue posible crear alumno. "+repr(e))
            del alumno
            return HttpResponseRedirect(reverse("crear_alumno"))
    
        return HttpResponseRedirect(reverse("crear_alumno"))


@staff_member_required()
def borrar_alumno(request, id_alumno=None): #Elimina alumno completamente, junto con user y actividad
    
    tipoAlumno = None

    if request.method == 'GET':
        try:
            alumno = Alumno.objects.get(id=id_alumno)
            tipoAlumno = alumno.es_Mechon
            id_usuario = alumno.usuario_id
            user = User.objects.get(id=id_usuario)
            user.delete()
            alumno.delete()

            if tipoAlumno:
                messages.success(request, '¡Alumno eliminado con éxito!')
                return HttpResponseRedirect(reverse("mechones"))
            else:
                messages.success(request, '¡Alumno eliminado con éxito!')
                return HttpResponseRedirect(reverse("padrinos"))
        
        except ObjectDoesNotExist:
            messages.error(request,'ERROR - ¡No se pudo eliminar al alumno correctamente!')
            return HttpResponseRedirect(reverse("handler500"))


@staff_member_required()
def updateAlumno(request): #Actualizar datos alumnos (NO HECHA)
    return redirect()






##############---------IMPORTACION----------###################
       
@permission_required('admin.can_add_log_entry')
def import_users(request): #Importar alumnos nuevos desde archivo .csv
    template = "contact_upload.html"

    prompt = {
        'order': 'Orden del csv deberia ser  rut, nombre, apellidos1, apellido2, generacion, email, emailPersonal'
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    if request.method == 'POST':
        try:
            csv_file = request.FILES["file"]
            if not csv_file.name.endswith('csv'):
                messages.error(request,'ERROR - ¡No es un archivo .csv!')
                return HttpResponseRedirect(reverse("import_users"))
            if csv_file.multiple_chunks():
                messages.error(request,"Archivo es demasiado grande (%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("import_users"))
            file_data = csv_file.read().decode("utf-8")	
            lines = file_data.split("\n")
            for line in lines:						
                fields = line.split(",")
                alumnoExiste = Alumno.objects.filter(rut=fields[0])
                
                if not alumnoExiste:
                    alumno = Alumno()
                    alumno.rut = fields[0]
                    alumno.nombre = fields[1]
                    alumno.apellidos = fields[2] + " " + fields[3] # AGREGAR CASO APELLIDOS = APELLIDO PATERNO + APELLIDO MATERNO
                    alumno.emailPersonal = fields[4]
                    alumno.email = fields[5]
                    alumno.carrera = fields[6]
                    alumno.generacion = fields[7]
                    if(date.today().year!=int(fields[7])):
                        alumno.es_Mechon = False
                    crearUser('', alumno.nombre, alumno.apellidos, alumno.emailPersonal)
                    usuario_alumno = User.objects.filter(email=alumno.emailPersonal)
                    alumno.usuario = usuario_alumno[0]
                    alumno.save()
                    del alumno
                
                now = date.today().year
                alumno_actual = Alumno.objects.get(rut=fields[0])
                actividad = Actividad.objects.filter(anno_participacion=now, alumno=alumno_actual)
                
                if not actividad:
               
                    actividad = Actividad()
                    actividad.alumno = Alumno.objects.get(rut=fields[0])
                    actividad.status = False
                    actividad.anno_participacion = now
                    if int(fields[7]) == now:
                        actividad.rol = 0
                    else:
                        actividad.rol = 1
                    actividad.save()

            messages.success(request, '¡Importación exitosa!')   
        
        except Exception as e:
            logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
            messages.error(request,"ERROR - No se pudo subir imagen. "+repr(e))
            redirect('import_users/')
        
       
        return HttpResponseRedirect(reverse("import_users"))

