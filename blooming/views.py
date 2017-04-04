from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, render
from random import choice
from content.models import *
from bloomerprofile.models import *
import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie

@never_cache
@ensure_csrf_cookie
def index(request):
  if request.user.is_authenticated():
    bloomer = Bloomer.objects.get(username=request.user.username)
    return render(request, 'blooming/index.html', {'bloomer':bloomer})
  else:
    return render(request, 'blooming/homepage.html')

def login_view(request):
    if request.user.is_authenticated():
        return redirect('blooming:index')
    if request.method == 'GET':
        return render(request, 'blooming/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request, 'Benvenut@ %s' % username)
            messages.success(request, "C'è un nuovo bottone «RiFormula», serve per sistemare le formule se vengono fuori formattate male.")
            return redirect('blooming:index')
        else:
            messages.error(request, 'Accesso non effettuato. Ritenta o contatta il tuo insegnante.')
            return redirect('blooming:index')

@login_required
def profile(request):
    return render(request, 'blooming/profile.html', {'bloomer':Bloomer.objects.get(username=request.user.username)})