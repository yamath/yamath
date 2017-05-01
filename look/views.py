from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from random import choice
from content.models import *
from bloomerprofile.models import *
import logging
import urllib
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from back.orm import *

@ensure_csrf_cookie
@login_required
def main(request):
    username=request.user.username
    return render(request, 'look/main.html')

@login_required
def html(request):
    username=request.user.username
    user = get('User', legacyUsername=username)
    command = request.GET.get('command')
    #print('look.views html', command, user)
    if command == '':
        pass
    elif command == 'error':
        return render(request, 'look/error.html')
#    elif command == 'loginForm':
#        return render(request, 'look/login.html')
    elif command == 'message':
        message = request.GET.get('message')
        return render(request, 'look/message.html', {'message':message})
    elif command == 'navbar':
        return render(request, 'look/navbar.html', {'user':user})
#    elif command == 'signupForm':
#        return render(request, 'look/signup.html')
    elif command == 'profile':
        classrooms = select('Classroom', lambda c: user in c.users)
        return render(request, 'look/profile.html', {'user':user, 'classrooms':classrooms})
    elif command == 'welcomeBoard':
        return render(request, 'look/welcomeBoard.html', {'user':user})
    else:
        raise Exception("/html unknown command")
    