from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
<<<<<<< Updated upstream
from .models import Usuario, Padrino, Mechon, Grupo, Afinacion, Encuesta, Resultado
=======
from usuarios.models import Alumno
from analisis.models import Grupo
from encuesta.models import Encuesta
import datetime
>>>>>>> Stashed changes

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


#PAGINAS CON SÓLO ACCESO DE ADMIN

@staff_member_required()
def listadoMechones(request):
    mechones = Alumno.objects.filter(es_Mechon=True)
	#return render(request, 'listadoMechones.html', {'mechones': mechones})
    return render(request, 'listadoMechones.html')


@staff_member_required()
def listadoPadrinos(request):
    padrinos = Alumno.objects.filter(es_Mechon=False)
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
            
<<<<<<< Updated upstream
            crearUser('post', nombre_alumno, apellidos_alumno, email_alumno)
            usuario_alumno = User.objects.filter(email=email_alumno)
            mechon.usuario = usuario_alumno[0]

            mechon.save()
            return HttpResponse('200 OK')
    
    return HttpResponse('404 OK')
=======
        crearUser('post', nombre_alumno, apellidos_alumno, email_alumno)
        usuario_alumno = User.objects.filter(email=email_alumno)
        alumno.usuario = usuario_alumno[0]
        alumno.save()
        confirmacion = True
        return render(request, 'crear_usuario.html', {'confirmacion' : confirmacion})

    confirmacion = False
    return render(request, 'crear_usuario.html', {'confirmacion' : confirmacion})
>>>>>>> Stashed changes
