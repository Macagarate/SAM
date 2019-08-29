from django.shortcuts import render
from .models import Preferencia
from usuarios.models import Actividad
from analisis.models import Respuesta
from matching.games.stable_marriage import StableMarriage
import operator
import textdistance

# Create your views here.
def index(request):


    calcular_preferencias()
    

    #for k,m  in matriz_mechones:
    




    """ a = get_ahijados()
    b = get_padrinos()
    solution =stableMarriage(b,a)"""
    return render(request, 'matchmaking.html')

def get_padrinos():
    padrinos = []
    persona_set  = Actividad.objects.filter(rol=1)
    for p in persona_set:
        aux = dict()
        lista_preferencias = []
        aux['user'] = p.id
        preferencias = Preferencia.objects.filter(pref_from=p).order_by('pref_order')
        for i in preferencias:
            lista_preferencias.append(i.id)
        aux['preferences'] = lista_preferencias
        padrinos.append(aux)
    return padrinos
def get_ahijados():
    ahijados = []
    persona_set  = Actividad.objects.filter(rol=0)
    for p in persona_set:
        aux = dict()
        lista_preferencias = []
        aux['user'] = p.id
        preferencias = Preferencia.objects.filter(pref_from=p).order_by('pref_order')
        for i in preferencias:
            lista_preferencias.append(i.id)
        aux['preferences'] = lista_preferencias 
        ahijados.append(aux)
    return ahijados

def stableMarriage(padrinos,ahijados):

    godparents = {}
    students = {}

    for padrino in padrinos:
        aux = []
        a = {}
        for pre in padrino['preferences']:
            aux.append(str(pre.pref_to.name))
        a[padrino['user']] = aux
        godparents.update(a)

    print(godparents)

    for ahijado in ahijados:
        aux = []
        a = {}
        for pre in ahijado['preferences']:
            aux.append(str(pre.pref_to.name))
        a[ahijado['user']] = aux
        students.update(a)

    print(students)

    game = StableMarriage.create_from_dictionaries(godparents, students)

    return game.solve()

def get_padrinos2():
    return Actividad.objects.filter(rol=1)

def get_ahijados2():
    return Actividad.objects.filter(rol=0)

def get_respuesta_encuesta(id_usuario):
    aux = ''
    respuestas = Respuesta.objects.filter(actividad=id_usuario)

    for r in respuestas:
        if (0<r.alternativa.id<=9):
            aux = aux +'0'+str(r.alternativa.id)+'-'         
        if (r.alternativa.id > 9):
            aux = aux +str(r.alternativa.id)+'-'
    return aux

def calcular_preferencias():
    alumno_padrinos = get_padrinos2()
    alumno_ahijados = get_ahijados2()
    matriz_mechones = list()
    matriz_padrinos = list()
    dicc_padrino = dict()
    dicc_mechon = dict()
    
    for i in alumno_padrinos:
        resultado_encuesta_p = get_respuesta_encuesta(i.id)
        print("Padrino", i.alumno)
        for j in alumno_ahijados:
            print("Ahijado", j.alumno)
            resultado_encuesta_m = get_respuesta_encuesta(j.id)
            afinidad = textdistance.hamming.normalized_similarity (resultado_encuesta_p, resultado_encuesta_m)
            dicc_padrino[i] = afinidad
            dicc_mechon[j]  = afinidad

            matriz_mechones = sorted(dicc_mechon.items(), key=operator.itemgetter(1), reverse = True)
            matriz_padrinos = sorted(dicc_padrino.items(), key=operator.itemgetter(1),reverse = True)
       
        cont = 1 
        for z  in matriz_mechones:
            preferencia = Preferencia()
            preferencia.pref_from = i
            preferencia.pref_to = z[0]
            preferencia.pref_order = cont
            #preferencia.save()
            cont = cont + 1
        cont = 1
        for z  in matriz_padrinos:
            preferencia = Preferencia()
            preferencia.pref_from = z[0]
            preferencia.pref_to = i
            preferencia.pref_order = cont
            #preferencia.save()
            cont = cont + 1
    solver_padrinos = get_padrinos()
    solver_ahijados = get_ahijados()
    print(solver_padrinos)
    print(solver_ahijados)

    capacidad = round(len(matriz_mechones)/len(matriz_padrinos))
    print(capacidad)