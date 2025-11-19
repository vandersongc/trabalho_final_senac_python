from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import constants as message_constants


# Create your views here.
def home(request):
    return render(request,'home.html')

def sobre(request):
    return render(request, 'sobre.html')

def login(request):
    return render(request, 'login.html')

def contato(request):
    return render(request, 'contato.html')

def admin(request):
    return render(request, 'admin.html')