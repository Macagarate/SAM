from django.shortcuts import render
from .models import Preferencia
from usuarios.models import Actividad
from matching.games.stable_marriage import StableMarriage

# Create your views here.
def index(request):
    a = get_ahijados()
    b = get_padrinos()
    solution =stableMarriage(b,a)
    return render(request, 'matchmaking.html',{'ahijados' : a,'padrinos' : b, 'solucion': solution.items()})

def get_padrinos():
    padrinos = []
    persona_set  = Actividad.objects.filter(rol=1)
    for p in persona_set:
        aux = dict()
        aux['user'] = p.alumno
        aux['preferences'] = Preferencia.objects.filter(pref_from=p).order_by('pref_order')
        padrinos.append(aux)
    return padrinos
def get_ahijados():
    ahijados = []
    persona_set  = Actividad.objects.filter(rol=0)
    for p in persona_set:
        aux = dict()
        aux['user'] = p.alumno
        aux['preferences'] = Preferencia.objects.filter(pref_from=p).order_by('pref_order')
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
