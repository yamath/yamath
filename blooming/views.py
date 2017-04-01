from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, render
from random import choice
from content.models import *
from bloomerprofile.models import *
#from blooming.models import *
#from django.contrib import messages
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
            messages.success(request, 'Benvenut@ %s' % username)
            return redirect('blooming:index')
        else:
            messages.error(request, 'Accesso non effettuato. Ritenta o contatta il tuo insegnante.')
            return redirect('blooming:index')

@login_required
def profile(request):
    return render(request, 'blooming/profile.html', {'bloomer':Bloomer.objects.get(username=request.user.username)})


# @never_cache
# @login_required
# def question(request, topic_pk):
#   bloomer = Bloomer.objects.get(user=request.user)
#   topic = Topic.objects.get(pk=topic_pk)
#   logging.info('Bloomer %s asked for topic %s' % (bloomer.user.username, topic.pk))
#   if request.method=='GET':
#     question = choice(topic.questions)
#     bloomer.add_scorevalue_of(topic, -20)
#     return render(request, 'blooming/question.html', {'bloomer':bloomer, 'topic':topic, 'question':question})
#   elif request.method == 'POST':
#     return redirect('blooming:submit')

# @never_cache
# @login_required
# def submit(request):
#     bloomer = Bloomer.objects.get(user=request.user)
#     question = Question.objects.get(pk=int(request.POST['question_pk']))
#     try:
#         answer = request.POST['answer']
#     except KeyError:
#         answer = ''
#     if question.kind in ['ibool', 'pbool']:
#         try:
#             status = Option.objects.filter(question=question, text=answer).first().status
#         except AttributeError:
#             status = 'r'
#         option = Option(user=bloomer.user, question=question, text=request.POST['answer'], status=status)
#     elif question.kind in ['imulti', 'pmulti']:
#         pk = [ key[7:] for (key, value) in request.POST.items() if key[:7]=='option_' ][0]
#         option = Option(user=bloomer.user, question=question, text=Option.objects.get(pk=pk).text, status=Option.objects.get(pk=pk).status)
#     else:
#         option = Option(user=bloomer.user, question=question, text=request.POST['answer'], status=question.get_status(request.POST['answer']))
#     option.save()
#     bloomer.add_scorevalue_of(question.topic, 0 if option.status == 'r' else +30)
#     logging.info('Bloomer %s answered %s to %s (%s)' % (bloomer.user.username, option.text, question.pk, option.status))
#     return render(request, 'blooming/submit.html', {'bloomer':bloomer, 'topic':question.topic, 'question':question, 'option':option})

