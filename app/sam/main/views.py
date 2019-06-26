from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def index(request): 
    return render(request, 'home.html')

@login_required()
def encuesta(request):
    return render(request, 'encuesta.html')

@login_required()
def perfil(request):
    return render(request, 'perfil.html')