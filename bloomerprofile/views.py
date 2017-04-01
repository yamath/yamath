# from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import never_cache
# from django.shortcuts import redirect, render
# from random import choice
# from content.models import *
# from blooming.models import *
import bloomerprofile.models as bloomingprofile
# from django.contrib import messages
# import logging
# from django.contrib import messages
# from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def ajax(request):
    print("BP AJAX:", request.POST)
    bloomer = bloomingprofile.Bloomer.objects.get(username=request.POST['username'])
    datadict = {}
    req_list = request.POST['request'].split()
    if 'done_series' in req_list:
        datadict['done_series'] = bloomer.get_series('done')
        print("Debug:", bloomer.get_series('done'))
    datadict['debug_message'] = "todo piola"
    return JsonResponse(datadict)
    # if request.user.is_authenticated():
    #     return redirect('blooming:index')
    # if request.method == 'GET':
    #     return render(request, 'blooming/login.html')
    # elif request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         messages.success(request, 'Benvenut@ %s' % username)
    #         return redirect('blooming:index')
    #     else:
    #         messages.error(request, 'Accesso non effettuato. Ritenta o contatta il tuo insegnante.')
    #         return redirect('blooming:index')