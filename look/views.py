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

def html(request, query):
    qdict = { q.split('=')[0].strip():q.split('=')[1].strip() for q in query.split(';') }
    command = qdict['command']
    try:
        bloomer = Bloomer.objects.get(username=qdict['username'])
    except:
        bloomer = None
    if command == '':
        pass
    elif command == 'error':
        return render(request, 'look/error.html')
    elif command == 'loginForm':
        return render(request, 'look/login.html')
    elif command == 'message':
        message = qdict['message']
        return render(request, 'look/message.html', {'message':message})
    elif command == 'navbar':
        return render(request, 'look/navbar.html', {'bloomer':bloomer})
    elif command == 'notlogin':
        return render(request, 'look/notlogin.html')
    elif command == 'welcomeBoard':
        return render(request, 'look/welcomeBoard.html', {'bloomer':bloomer})
    else:
        raise Exception("/html unknown command")
    