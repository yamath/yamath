from django.contrib.auth import authenticate
from django.http import HttpResponse

def back(request, query):
    qdict = { q.split('=')[0].strip():q.split('=')[1].strip() for q in query.split(';') }
    command = qdict['command']
    if command == 'login':
        
        user = authenticate(username=qdict['username'], password=qdict['password'])
        if user is not None:
            return HttpResponse('', status=200)
        else:
            return HttpResponse('', status=400)