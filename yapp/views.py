from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from random import choice
from .models import Question, Score, Topic, TopicDependency, Answer
from django.contrib import messages

def index(request):
  if request.user.is_authenticated():
    username = request.user.username
    info = []
    for t in Topic.objects.all():
      try:
        question = choice(Question.objects.filter(topic=t))
      except:
        question = None
      try:
        score_value = int(Score.objects.get(user=username, topic=t).value)
      except Score.DoesNotExist:
        score_value = 0
      if score_value > 90:
        topic_status = 'ok'
      elif all( int(Score.objects.get(user=username, topic=dep.ante).value)>90 for dep in TopicDependency.objects.filter(post=t)):
        topic_status = 'todo'
      else:
        topic_status = 'far'
      info.append((t, question, score_value, topic_status))
      info = sorted(info, lambda x: 1 if x[3]=='ok' else (2 if x[3]=='todo' else 3))
    return render(request, 'index.html', {'info':info})
  else:
    return render(request, 'index.html')

@login_required
def question(request, topic_serial):
  topic = Topic.objects.get(serial=topic_serial)
  try:
    score = Score.objects.get(user=request.user.username, topic=topic)
  except Score.DoesNotExist:
    score = Score(user=request.user.username, topic=topic_label, value=0)
  if 'question' not in request.session:
    question = choice(Question.objects.filter(topic=topic))
    request.session['question'] = question
    return render(request, 'question.html', {'question':question})
  else:
    try:
      Answer.objects.get(question=request.session['question'], answer=request.POST['answer'], status='ok')
      score.value = min(100, score.value+10)
      messages.add_message(request, messages.SUCCESS, 'Risposta esatta!')
    except:
      score.value = max(0, score.value-20)
      messages.add_message(request, messages.ERROR, 'Risposta sbagliata.')
    score.save()
    return redirect('index')
