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
def main(request):
    if request.user.is_authenticated():
        bloomer = Bloomer.objects.get(username=request.user.username)
    else:
        bloomer = None
    return render(request, 'look/main.html', {'bloomer':bloomer})