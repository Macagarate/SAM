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
from usuarios.models import Alumno
from analisis.models import Grupo
from encuesta.models import Encuesta
import datetime 
from datetime import date
import logging
from django.urls import reverse
from django.template import *


##############---------FUNCIONES HANDLERS----------####################

def handler404(request):
    return render(request, '404.html', status=404)
    
def handler500(request):
    return render(request, '500.html', status=500)



def crearUser(request, nombre=None, apellido=None, email=None): #Creacion de nuevos usuarios
    
    # PARA EVITAR PROBLEMAS CON LETRAS ESPECIALES Y TILDES #
    a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
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

def enviarEncuesta(request):
    return HttpResponse('')


##############---------FUNCIONES DE RENDER----------####################


@login_required()
def index(request):
    return render(request, 'home.html')


@login_required()
def encuesta(request):
    return render(request, 'encuesta.html')


@login_required()
def perfil(request):
    perfil = Alumno.objects.get(usuario=request.user.id)
    return render(request, 'perfil.html', {'perfil': perfil})


@login_required()
def resultadoEncuesta(request):
    return render(request, 'resultado-encuesta.html')


@login_required()
def grupo(request):
    return render(request, 'grupo.html')

@login_required()
def cambiar_pass(request):
    template = "cambiar_pass.html"

    prompt = {
    }

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


#----------------PAGINAS CON SÓLO ACCESO DE ADMIN!


@staff_member_required()
def listadoMechones(request):
    mechones = Alumno.objects.filter(es_Mechon=True)
    return render(request, 'listadoMechones.html', {'mechones': mechones})


@staff_member_required()
def listadoPadrinos(request):
    padrinos = Alumno.objects.filter(es_Mechon=False)
    return render(request, 'listadoPadrinos.html', {'padrinos': padrinos})


@staff_member_required()
def grupos(request):
    grupos = Grupo.objects.all()
    return render(request, 'grupos.html', {'grupos': grupos})
    #return render(request, 'grupos.html')

##############---------CRUD ENCUESTA----------###################

@staff_member_required()
def resultadosEncuestas(request):
    alumnos = Alumno.objects.all()
    return render(request, 'resultados-encuestas.html', {'alumnos': alumnos})


@staff_member_required()
def encuestas(request):
    encuestas = Encuesta.objects.all()
    return render(request, 'encuestas.html',{'encuestas': encuestas})

@staff_member_required()
def crearEncuesta(request):
    encuesta = Encuesta()
    if request.method == 'POST':
        anno = request.POST.get('annio')
        encuesta.anno = datetime.date(int(anno),1,1)
        encuesta.save()
        return redirect('encuestas')

@staff_member_required()
def verEncuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    return render(request,'encuesta_ver.html',{'encuesta': encuesta})

@staff_member_required()
def editarEncuesta(request):  
    return redirect()

@staff_member_required()
def updateEncuesta(request):
    return redirect()

@staff_member_required()
def eliminarEncuesta(request):
    return redirect()


##############---------CRUD USUARIOS----------###################

@staff_member_required()
def crear_alumno(request):
    template = "crear_usuario.html"

    prompt = {
    }

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
                messages.success(request, '¡Alumno agregado con éxito!')
                del alumno
            else:
                messages.error(request,'ERROR - Alumno no pudo ser creado')
                del alumno
                return HttpResponseRedirect(reverse("crear_alumno"))

        except Exception as e:
            messages.error(request,"No fue posible crear alumno. "+repr(e))
            del alumno
            return HttpResponseRedirect(reverse("crear_alumno"))
    
        return HttpResponseRedirect(reverse("crear_alumno"))


@staff_member_required()
def borrar_alumno(request, id_alumno=None):
    
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



##############---------IMPORTACION----------###################
       
@permission_required('admin.can_add_log_entry')
def import_users(request):
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
            messages.success(request, '¡Importación exitosa!')   
        
        except Exception as e:
            logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
            messages.error(request,"ERROR - No se pudo subir imagen. "+repr(e))
            redirect('import_users/')
        
       
        return HttpResponseRedirect(reverse("import_users"))

