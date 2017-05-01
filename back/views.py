import hashlib
import smtplib
from back.orm import *
from django.contrib.auth import authenticate
from django.http import HttpResponse
from email.mime.text import MIMEText
from back.legacy import derive


def back(request):
    command = request.GET.get('command')
    if command == 'login':
        ### non funzionerà
        try:
            user = get('User',
                       email=request.GET.get('email'),
                       phash = hashlib.blake2b(('salt:'+request.GET.get('password')).encode(), digest_size=16).hexdigest())
        except Exception as e:
            print('back login', e)
            user = None
        if user is not None:
            return HttpResponse(user.email, status=200)
        else:
            return HttpResponse('', status=400)
    if command == 'signup':
        email = request.GET.get('email')
        pplain = request.GET.get('password')
        phash = hashlib.blake2b(('salt:'+pplain).encode(), digest_size=16).hexdigest()
        print('back signup', email, phash)
        try:
            newUser = new('User', email=email, phash=phash, status='pend')
            secret = hashlib.blake2b(('salt:'+email).encode(), digest_size=16).hexdigest()
            msg = MIMEText("<p>Ci hanno richiesto un profilo a nome di questo indirizzo. Se non sei l'autore di tale richiesta per favore cancella questa mail e dimentica l'accaduto. Se hai richiesto tu il profilo, attivalo seguendo questo <a href='http://yamath.pythonanywhere.com/experimental/back/command=activate&secret={1}'>link di attivazione</a>.</p>".format(email, secret), 'html')
            msg['Subject'] = 'Attivazione account yamath'
            msg['From'] = 'bloomingmath@zoho.com'
            msg['To'] = email
            server = smtplib.SMTP('smtp.zoho.com:587')
            server.ehlo()
            server.starttls()
            server.login('bloomingmath@zoho.com', 'ichigoichie')
            server.send_message(msg)
            server.quit()
            return HttpResponse('', status=200)
        except Exception as e:
            print("back signup", e)
            return HttpResponse('', status=400)
            
derive()