from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, render
from random import choice
from content.models import *
from blooming.models import *
#from django.contrib import messages
import logging

@never_cache
def index(request):
  if request.user.is_authenticated():
    bloomer = Bloomer.objects.get(user=request.user)
    info = set()
    for t in bloomer.topics:
      score_value = bloomer.get_scorevalue_of(t)
      if score_value > 90:
        topic_status = 'ok'
      elif all( bloomer.get_scorevalue_of(ante)>90 for ante in t.antes):
        topic_status = 'todo'
      else:
        topic_status = 'far'
      info.add((t, score_value, topic_status))
    info = sorted(info, key=lambda x: 1 if x[2]=='ok' else (2 if x[2]=='todo' else 3))
    return render(request, 'profile.html', {'info':info, 'bloomer':bloomer})
  else:
    return render(request, 'homepage.html')

@never_cache
@login_required
def question(request, topic_pk):
  bloomer = Bloomer.objects.get(user=request.user)
  topic = Topic.objects.get(pk=topic_pk)
  logging.info('Bloomer %s asked for topic %s' % (bloomer.user.username, topic.pk))
  if request.method=='GET':
    question = choice(topic.questions)
    bloomer.add_scorevalue_of(topic, -20)
    return render(request, 'blooming/question.html', {'bloomer':bloomer, 'topic':topic, 'question':question})
  elif request.method == 'POST':
    return redirect('blooming:submit')

@never_cache
@login_required
def submit(request):
    bloomer = Bloomer.objects.get(user=request.user)
    question = Question.objects.get(pk=int(request.POST['question_pk']))
    try:
        answer = request.POST['answer']
    except KeyError:
        answer = ''
    if question.kind in ['ibool', 'pbool']:
        try:
            status = Option.objects.filter(question=question, text=answer).first().status
        except AttributeError:
            status = 'r'
        option = Option(user=bloomer.user, question=question, text=request.POST['answer'], status=status)
    elif question.kind in ['imulti', 'pmulti']:
        pk = [ key[7:] for (key, value) in request.POST.items() if key[:7]=='option_' ][0]
        option = Option(user=bloomer.user, question=question, text=Option.objects.get(pk=pk).text, status=Option.objects.get(pk=pk).status)
    else:
        option = Option(user=bloomer.user, question=question, text=request.POST['answer'], status=question.get_status(request.POST['answer']))
    option.save()
    bloomer.add_scorevalue_of(question.topic, 0 if option.status == 'r' else +30)
    logging.info('Bloomer %s answered %s to %s (%s)' % (bloomer.user.username, option.text, question.pk, option.status))
    return render(request, 'blooming/submit.html', {'bloomer':bloomer, 'topic':question.topic, 'question':question, 'option':option})

