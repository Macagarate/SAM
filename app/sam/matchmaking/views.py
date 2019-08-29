from django.shortcuts import render
from .models import Preferencia
from usuarios.models import Actividad
from analisis.models import Respuesta
from analisis.models import Grupo
from matching.games.hospital_resident import HospitalResident
import operator
import textdistance

# Create your views here.
def index(request):

    solver_padrinos = []
    solver_ahijados = []
    solution = []

    calcular_preferencias_padrino()
    calcular_preferencias_ahijado()

    solver_ahijados = generate_dict_ahijados()
    solver_padrinos = generate_dict_padrinos()
    #print(solver_ahijados)
    #print("\n")
    #print(solver_padrinos)

    solution = stableMarriage(solver_padrinos,solver_ahijados)
    guardar_grupo(solution)

    return render(request, 'matchmaking.html')

def guardar_grupo(solucion_matchmaking):
    cont=1
    for x in solucion_matchmaking.items():
        padrino = Actividad.objects.filter(id=str(x[0]))
        for a in x[1]:
            grupo = Grupo()
            ahijado = Actividad.objects.filter(id=str(a))
            grupo.padrino = padrino[0].alumno
            grupo.ahijado = ahijado[0].alumno
            grupo.numero = cont
            grupo.save()
        cont = cont + 1




def calcular_preferencias_padrino():
    alumno_padrinos = get_padrinos2()
    alumno_ahijados = get_ahijados2()
    matriz_mechones = list()
    dicc_mechon = dict()
    
    for i in alumno_padrinos:
        resultado_encuesta_p = get_respuesta_encuesta(i.id)
        
        for j in alumno_ahijados:
            resultado_encuesta_m = get_respuesta_encuesta(j.id)
            afinidad = textdistance.hamming.normalized_similarity (resultado_encuesta_p, resultado_encuesta_m)
            dicc_mechon[j]  = afinidad

        matriz_mechones = sorted(dicc_mechon.items(), key=operator.itemgetter(1), reverse = True)
        guardar_preferencia(i,matriz_mechones)
    
def calcular_preferencias_ahijado():
    alumno_padrinos = get_padrinos2()
    alumno_ahijados = get_ahijados2()
    matriz_mechones = list()
    dicc_mechon = dict()
    
    for i in alumno_ahijados:
        resultado_encuesta_p = get_respuesta_encuesta(i.id)
        for j in  alumno_padrinos:
            resultado_encuesta_m = get_respuesta_encuesta(j.id)
            afinidad = textdistance.hamming.normalized_similarity (resultado_encuesta_p, resultado_encuesta_m)
            dicc_mechon[j]  = afinidad
        matriz_mechones = sorted(dicc_mechon.items(), key=operator.itemgetter(1), reverse = True)
        guardar_preferencia(i,matriz_mechones)

def guardar_preferencia(desde:Actividad,matriz_preferencia):
    cont=1
    for i in matriz_preferencia:
        preferencia = Preferencia()
        preferencia.pref_from = desde
        preferencia.pref_to = i[0]
        preferencia.pref_order = cont
        preferencia.save()
        cont = cont +1

def generate_dict_padrinos():
    padrinos = []
    persona_set  = Actividad.objects.filter(rol=1)
    for p in persona_set:
        aux = dict()
        lista_preferencias = []
        aux['user'] = p.id
        preferencias = Preferencia.objects.filter(pref_from=p).order_by('pref_order')
        for i in preferencias:
            lista_preferencias.append(i.pref_to.id)
        aux['preferences'] = lista_preferencias
        padrinos.append(aux)
    return padrinos
def generate_dict_ahijados():
    ahijados = []
    persona_set  = Actividad.objects.filter(rol=0)
    for p in persona_set:
        aux = dict()
        lista_preferencias = []
        aux['user'] = p.id
        preferencias = Preferencia.objects.filter(pref_from=p).order_by('pref_order')
        for i in preferencias:
            lista_preferencias.append(i.pref_to.id)
        aux['preferences'] = lista_preferencias 
        ahijados.append(aux)
    return ahijados

def stableMarriage(padrinos,ahijados):

    hospital_prefs = {}
    resident_prefs = {}

    for padrino in padrinos:
        aux = []
        a = dict()
        for pre in padrino['preferences']:
            aux.append(str(pre))
        a[str(padrino['user'])] = aux
        hospital_prefs.update(a)
    
    for ahijado in ahijados:
        aux = []
        a = dict()
        for pre in ahijado['preferences']:
            aux.append(str(pre))
        a[str(ahijado['user'])] = aux
        resident_prefs.update(a)
    
    capacities = {hosp: 2 for hosp in hospital_prefs}
    game = HospitalResident.create_from_dictionaries(resident_prefs, hospital_prefs,capacities)
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

