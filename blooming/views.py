from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, render
from random import choice, shuffle
from .models import Bloomer, Classroom, Topic, Question, Option, Score, Collection
from django.contrib import messages

def index(request):
#  try:
#    del request.session['question_pk']
#  except:
#    pass
  if request.user.is_authenticated():
#    user = request.user
    bloomer = Bloomer.objects.get(user=request.user)
    info = set()
#    topics = []
#    for cu in ClassroomUser.objects.filter(user=user):
#        for tc in TopicClassroom.objects.filter(classroom=cu.classroom):
#            topics.append(tc.topic)
#    topics = list(set(topics))
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

#    session_user = user.username
#    if 'session_topic' in request.session:
#        session_topic = request.session['session_topic']
#    else:
#        session_topic = 'none'
#    if 'session_questionpk' in request.session:
#        session_questionpk = request.session['session_questionpk']
#    else:
#        session_questionpk = 0
#    if 'session_answer' in request.session:
#        session_answer = request.session['session_answer']
#    else:
#        session_answer = 'none'
    return render(request, 'blooming/index.html', {'info':info})#, 'session_user':session_user, 'session_topic':session_topic, 'session_questionpk':session_questionpk, 'session_answer':session_answer})
  else:
    return render(request, 'blooming/index.html')

@never_cache
@login_required
def question(request, topic_pk):
  bloomer = Bloomer.objects.get(user=request.user)
  topic = Topic.objects.get(pk=topic_pk)
  if request.method=='GET':
    questions_list = topic.questions
    question = choice(questions_list)
    bloomer.add_scorevalue_of(topic, -20)
    return render(request, 'blooming/question.html', {'question':question, 'bloomer':bloomer})
  else:
    return redirect('blooming:submit')

@never_cache
@login_required
def submit(request):
    bloomer = Bloomer.objects.get(user=request.user)
    question = Question.objects.get(pk=int(request.POST['question_pk']))
    option = Option(user=bloomer.user, question=question, text=request.POST['answer'], status=question.get_status(request.POST['answer']))
    option.save()
    bloomer.add_scorevalue_of(question.topic, 0 if option.status == 'r' else +30)
    return render(request, 'blooming/submit.html', {'question':question, 'option':option})

def claim(request):
    Claim(username=request.POST['session_user'], questionpk=request.POST['session_questionpk'], topic=request.POST['session_topic'], answer=request.POST['session_answer']).save()
    messages.add_message(request, messages.SUCCESS, 'Grazie per la collaborazione!')
    return redirect('index')

def tools_add_questionmultiple(request):
    if request.method == 'GET':
        return render(request, 'add_questionmultiple.html')
    elif request.method == 'POST':
        qm = QuestionMultiple(topic=Topic.objects.get(serial=request.POST['topic_serial']), text=request.POST['text'], notes=request.POST['notes'])
        qm.save()
        for i in range(1, 7):
            if request.POST['true_option'+str(i)]!='':
                o = Option(text=request.POST['true_option'+str(i)], status=True)
                o.save()
                qm.options.add(o)
            if request.POST['false_option'+str(i)]!='':
                o = Option(text=request.POST['false_option'+str(i)], status=False)
                o.save()
                qm.options.add(o)
        return render(request, 'add_questionmultiple.html', {'topic_serial':request.POST['topic_serial']})