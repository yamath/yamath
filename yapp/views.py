from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, render
from random import choice
from .models import Classroom, ClassroomUser, Topic, Score, TopicClassroom, TopicDependency, Option, QuestionMultiple, QuestionBoolean, QuestionOpen, Claim
from django.contrib import messages

def index(request):
  def score_or_0(user, topic):
    try:
      return int(Score.objects.get(user=user, topic=topic).value)
    except:
      return 0
  try:
    del request.session['question_pk']
  except:
    pass
  if request.user.is_authenticated():
    user = request.user
    classroom = ClassroomUser.objects.get(user=user).classroom
    info = []
    for tc in TopicClassroom.objects.filter(classroom=classroom):
      t = tc.topic
      score_value = score_or_0(user=user, topic=t)
      if score_value > 90:
        topic_status = 'ok'
      elif all( score_or_0(user=user, topic=dep.ante)>90 for dep in TopicDependency.objects.filter(post=t)):
        topic_status = 'todo'
      else:
        topic_status = 'far'
      info.append((t, score_value, topic_status))
      info = sorted(info, key=lambda x: 1 if x[2]=='ok' else (2 if x[2]=='todo' else 3))

    session_user = user.username
    if 'session_topic' in request.session:
        session_topic = request.session['session_topic']
    else:
        session_topic = 'none'
    if 'session_questionpk' in request.session:
        session_questionpk = request.session['session_questionpk']
    else:
        session_questionpk = 0
    if 'session_answer' in request.session:
        session_answer = request.session['session_answer']
    else:
        session_answer = 'none'
    return render(request, 'index.html', {'info':info, 'session_user':session_user, 'session_topic':session_topic, 'session_questionpk':session_questionpk, 'session_answer':session_answer})
  else:
    return render(request, 'index.html')

@never_cache
@login_required
def question(request, topic_serial):
  topic = Topic.objects.get(serial=topic_serial)
  if 'question_pk' not in request.session:
    question = choice(QuestionOpen.objects.filter(topic=topic))
    request.session['question_pk'] = question.pk
    return render(request, 'question.html', {'question':question, 'topic':topic, 'session_user':request.user.username, 'session_topic':topic.serial, 'session_questionpk':question.pk, 'session_answer':''})
  else:
    try:
      score = Score.objects.get(user=request.user, topic=topic)
    except Score.DoesNotExist:
      score = Score(user=request.user, topic=topic, value=0)
    options = QuestionOpen.objects.get(pk=request.session['question_pk']).options.all()
    try:
      if options.get(text=request.POST['answer']).status:
        score.value = min(100, score.value+10)
        messages.add_message(request, messages.SUCCESS, 'Risposta esatta!')
      else:
        raise ValueError
    except:
      score.value = max(0, score.value-20)
      messages.add_message(request, messages.ERROR, 'Risposta sbagliata.')
    score.save()
    qpk = request.session['question_pk']
    del request.session['question_pk']
    request.session['session_user'] = request.user.username
    request.session['session_topic'] = topic.serial
    request.session['session_questionpk'] = qpk
    request.session['session_answer'] = request.POST.get('answer', '')
    return redirect('index')

def claim(request):
    Claim(username=request.POST['session_user'], questionpk=request.POST['session_questionpk'], topic=request.POST['session_topic'], answer=request.POST['session_answer']).save()
    messages.add_message(request, messages.SUCCESS, 'Grazie per la collaborazione!')
    return redirect('index')
