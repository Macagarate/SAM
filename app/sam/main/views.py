import csv, io  
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from usuarios.models import Alumno
from analisis.models import Grupo
from encuesta.models import Encuesta
import datetime 
from datetime import date
import logging
from django.urls import reverse


##############---------FUNCIONES HANDLERS----------####################

def handler404(request):
    return render(request, '404.html', status=404)
    
def handler500(request):
    return render(request, '500.html', status=500)

#Creacion de nuevos usuarios; NO RETORNA UN TEMPLATE

def crearUser(request, nombre=None, apellido=None, email=None):
    
    # PARA EVITAR PROBLEMAS CON LETRAS ESPECIALES Y TILDES #
    a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
    trans = str.maketrans(a,b)
    nombre_nuevo = nombre.translate(trans)
    apellido_nuevo = apellido.translate(trans)

    first_letra = nombre_nuevo[:1].lower()
    apellidoSplit = apellido_nuevo.split(" ")
    first_apellido = apellidoSplit[0].lower()
    second_apellido = apellidoSplit[1][:1].lower()
    
    userName = first_letra + first_apellido + second_apellido
    userExiste = User.objects.filter(username=userName)
    if userExiste == None:
        userPass = userName + '99'
        userEmail = email

        user = User.objects.create_user(username=userName,
                                        email=userEmail,
                                        password=userPass)
        user.save()
        del user

    return HttpResponse('')

#Recibe encuesta lista de un alumno

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


@staff_member_required()
def resultadosEncuestas(request):
    return render(request, 'resultados-encuestas.html')


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

@staff_member_required()
def nuevoAlumno(request):
    confirmacion = None
    return render(request, 'crear_usuario.html', {'confirmacion' : confirmacion})


@staff_member_required()
def crear_alumno(request):
    
    if request.method == 'POST':
        alumno = Alumno()
        nombre_alumno = request.POST.get('inputNombre')
        apellidos_alumno = request.POST.get('inputApellido')
        email_alumno = request.POST.get('inputEmail1')

        alumno.nombre = nombre_alumno
        alumno.apellidos = apellidos_alumno
        alumno.rut = request.POST.get('inputRut')
        alumno.generacion = request.POST.get('inputGeneracion')
        alumno.email = email_alumno
        alumno.emailPersonal = request.POST.get('inputEmail2')
        
        if request.POST.get('inputTipo') == 'PADRINO':
            alumno.es_Mechon =  False
        
        else:
             alumno.es_Mechon =  True
            
        crearUser('post', nombre_alumno, apellidos_alumno, email_alumno)
        usuario_alumno = User.objects.filter(email=email_alumno)
        alumno.usuario = usuario_alumno[0]
        alumno.save()
        confirmacion = True

        return render(request, 'crear_usuario.html', {'confirmacion' : confirmacion})

    return HttpResponse('404 OK')



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
                messages.error(request,'No es un archivo csv')
                return HttpResponseRedirect(reverse("import_users"))
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("import_users"))
            file_data = csv_file.read().decode("utf-8")	
            lines = file_data.split("\n")
            for line in lines:						
                fields = line.split(",")
                alumnoExiste = Alumno.objects.filter(rut=fields[0])
                if alumnoExiste == None:
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
               
        except Exception as e:
            logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
            messages.error(request,"Unable to upload file. "+repr(e))
            redirect('import_users/')
        return HttpResponseRedirect(reverse("import_users"))

