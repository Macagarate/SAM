from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from usuarios.models import Usuario, Padrino, Mechon
from .models import Grupo,Afinacion, Resultado
from encuesta.models import Encuesta

##############---------FUNCIONES POR IMPLEMENTAR----------####################

#Creacion de nuevos usuarios; NO RETORNA UN TEMPLATE

def crearUser(request, nombre=None, apellido=None, email=None):
    
    first_letra = nombre[:1].lower()
    apellidoSplit = apellido.split(" ")
    first_apellido = apellidoSplit[0].lower()
    second_apellido = apellidoSplit[1][:1].lower()
    
    userName = first_letra + first_apellido + second_apellido
    userPass = userName + '99'
    userEmail = email

    user = User.objects.create_user(username=userName,
                                    email=userEmail,
                                    password=userPass)
    user.save()

    return HttpResponse('')

#Recibe encuesta lista de un alumno

def enviarEncuesta(request):
    return HttpResponse('')


##############---------FUNCIONES DE RENDER----------####################


@login_required()
def index(request):
    perfil = Usuario.objects.get(usuario=request.user.id)

    return render(request, 'home.html', {'perfil': perfil})


@login_required()
def encuesta(request):
    return render(request, 'encuesta.html')


@login_required()
def perfil(request):

    perfil = Usuario.objects.get(usuario=request.user.id)

    return render(request, 'perfil.html', {'perfil': perfil})


@login_required()
def resultadoEncuesta(request):
    return render(request, 'resultado-encuesta.html')


@login_required()
def grupo(request):
    return render(request, 'grupo.html')


#PAGINAS CON SÓLO ACCESO DE ADMIN

@staff_member_required()
def listadoMechones(request):
    mechones = Mechon.objects.all()
	#return render(request, 'listadoMechones.html', {'mechones': mechones})
    return render(request, 'listadoMechones.html')


@staff_member_required()
def listadoPadrinos(request):
    padrinos = Padrino.objects.all()
	#return render(request, 'listadoPadrinos.html', {'padrinos': padrinos})
    return render(request, 'listadoPadrinos.html')


@staff_member_required()
def grupos(request):
    grupos = Grupo.objects.all()
    #return render(request, 'grupos.html', {'grupos': grupos})
    return render(request, 'grupos.html')


@staff_member_required()
def resultadosEncuestas(request):
    return render(request, 'resultados-encuestas.html')


@staff_member_required()
def encuestas(request):
    return render(request, 'encuestas.html')


@staff_member_required()
def nuevoAlumno(request):
    return render(request, 'crear_usuario.html')


@staff_member_required()
def crear_alumno(request):
    
    if request.method == 'POST':
        nombre_alumno =request.POST.get('inputNombre')
        apellidos_alumno = request.POST.get('inputApellido')
        rut_alumno = request.POST.get('inputRut')
        generacion_alumno = request.POST.get('inputGeneracion')
        email_alumno = request.POST.get('inputEmail1')
        emailPersonal_alumno = request.POST.get('inputEmail2')
        
        if request.POST.get('inputTipo') == 'PADRINO':

            padrino = Padrino()
            padrino.nombre = nombre_alumno
            padrino.apellidos = apellidos_alumno
            padrino.rut = rut_alumno
            padrino.generacion = generacion_alumno
            padrino.email = email_alumno
            padrino.emailPersonal = emailPersonal_alumno

            crearUser(nombre_alumno, apellidos_alumno, email_alumno)
            usuario_alumno = User.objects.filter(email=email_alumno)

            padrino.save()
            return HttpResponse('200 OK')


        if request.POST.get('inputTipo') == 'MECHON':

            mechon = Mechon()
            mechon.nombre = nombre_alumno
            mechon.apellidos = apellidos_alumno
            mechon.rut = rut_alumno
            mechon.generacion = generacion_alumno
            mechon.email = email_alumno
            mechon.emailPersonal = emailPersonal_alumno
            
            crearUser('post', nombre_alumno, apellidos_alumno, email_alumno)
            usuario_alumno = User.objects.filter(email=email_alumno)
            mechon.usuario = usuario_alumno[0]

            mechon.save()
            return HttpResponse('200 OK')
    
    return HttpResponse('404 OK')