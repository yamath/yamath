from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from random import choice
from .models import Question, Score, Topic, TopicDependency, Answer
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
    info = []
    for t in Topic.objects.all():
      score_value = score_or_0(user=user, topic=t)
      if score_value > 90:
        topic_status = 'ok'
      elif all( score_or_0(user=user, topic=dep.ante)>90 for dep in TopicDependency.objects.filter(post=t)):
        topic_status = 'todo'
      else:
        topic_status = 'far'
      info.append((t, score_value, topic_status))
      info = sorted(info, key=lambda x: 1 if x[2]=='ok' else (2 if x[2]=='todo' else 3))
    return render(request, 'index.html', {'info':info})
  else:
    return render(request, 'index.html')

def index_3M(request):
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
    info = []
    for t in Topic.objects.all():
      score_value = score_or_0(user=user, topic=t)
      if score_value > 90:
        topic_status = 'ok'
      elif all( score_or_0(user=user, topic=dep.ante)>90 for dep in TopicDependency.objects.filter(post=t)):
        topic_status = 'todo'
      else:
        topic_status = 'far'
      info.append((t, score_value, topic_status))
      info = sorted(info, key=lambda x: 1 if x[2]=='ok' else (2 if x[2]=='todo' else 3))
    return render(request, 'index_3M.html', {'info':info})
  else:
    return render(request, 'index.html')

def index_1A(request):
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
    info = []
    for t in Topic.objects.all():
      score_value = score_or_0(user=user, topic=t)
      if score_value > 90:
        topic_status = 'ok'
      elif all( score_or_0(user=user, topic=dep.ante)>90 for dep in TopicDependency.objects.filter(post=t)):
        topic_status = 'todo'
      else:
        topic_status = 'far'
      info.append((t, score_value, topic_status))
      info = sorted(info, key=lambda x: 1 if x[2]=='ok' else (2 if x[2]=='todo' else 3))
    return render(request, 'index_1A.html', {'info':info})
  else:
    return render(request, 'index.html')

def index_2A(request):
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
    info = []
    for t in Topic.objects.all():
      score_value = score_or_0(user=user, topic=t)
      if score_value > 90:
        topic_status = 'ok'
      elif all( score_or_0(user=user, topic=dep.ante)>90 for dep in TopicDependency.objects.filter(post=t)):
        topic_status = 'todo'
      else:
        topic_status = 'far'
      info.append((t, score_value, topic_status))
      info = sorted(info, key=lambda x: 1 if x[2]=='ok' else (2 if x[2]=='todo' else 3))
    request.session['classe'] = '2A'
    return render(request, 'index_2A.html', {'info':info})
  else:
    return render(request, 'index.html')

def index_2S(request):
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
    info = []
    for t in Topic.objects.all():
      score_value = score_or_0(user=user, topic=t)
      if score_value > 90:
        topic_status = 'ok'
      elif all( score_or_0(user=user, topic=dep.ante)>90 for dep in TopicDependency.objects.filter(post=t)):
        topic_status = 'todo'
      else:
        topic_status = 'far'
      info.append((t, score_value, topic_status))
      info = sorted(info, key=lambda x: 1 if x[2]=='ok' else (2 if x[2]=='todo' else 3))
    request.session['classe'] = '2S'
    return render(request, 'index_2S.html', {'info':info})
  else:
    return render(request, 'index.html')

@login_required
def question(request, topic_serial):
  topic = Topic.objects.get(serial=topic_serial)
  if 'question_pk' not in request.session:
    question = choice(Question.objects.filter(topic=topic))
    request.session['question_pk'] = question.pk
    return render(request, 'question.html', {'question':question, 'topic':topic})
  else:
    try:
      score = Score.objects.get(user=request.user, topic=topic)
    except Score.DoesNotExist:
      score = Score(user=request.user, topic=topic, value=0)
    try:
      Answer.objects.get(question=Question.objects.get(pk=request.session['question_pk']), answer=request.POST['answer'], status='ok')
      score.value = min(100, score.value+10)
      messages.add_message(request, messages.SUCCESS, 'Risposta esatta!')
    except:
      score.value = max(0, score.value-20)
      messages.add_message(request, messages.ERROR, 'Risposta sbagliata.')
    score.save()
    del request.session['question_pk']
    if 'classe' not in request.session:
        return redirect('index')
    elif request.session['classe']=='2A':
        return redirect('seconda_artistico')
    elif request.session['classe']=='2S':
        return redirect('seconda_scientifico')
    else:
        return redirect('index')
