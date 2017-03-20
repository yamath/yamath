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
    request.session['question_pk'] = question.pk
#    if isinstance(question, QuestionMultiple ):
#        request.session['question_type'] = 'multiple'
#        question_options = list(question.options.all())[:]
#        shuffle(question_options)
#        return render(request, 'question_multiple.html', {'question':question, 'question_options':question_options, 'topic':topic, 'session_user':request.user.username, 'session_topic':topic.serial, 'session_questionpk':question.pk, 'session_answer':''})
#    elif isinstance(question, QuestionBoolean):
#        request.session['question_type'] = 'boolean'
#        return render(request, 'question_boolean.html', {'question':question, 'topic':topic, 'session_user':request.user.username, 'session_topic':topic.serial, 'session_questionpk':question.pk, 'session_answer':''})
#    elif isinstance(question, QuestionOpen):
#        request.session['question_type'] = 'open'
#        return render(request, 'question.html', {'question':question, 'topic':topic, 'session_user':request.user.username, 'session_topic':topic.serial, 'session_questionpk':question.pk, 'session_answer':''})
    return render(request, 'question.html', {'question':question, 'bloomer':bloomer})
  else:
    try:
      score = Score.objects.get(user=request.user, topic=topic)
    except Score.DoesNotExist:
      score = Score(user=request.user, topic=topic, value=0)
    scorevalue = bloomer.get_scorevalue_of(topic)
    if request.session['question_type']=='multiple':
        question = QuestionMultiple.objects.get(pk=request.session['question_pk'])
        options = question.options.all()
        correct = True
        #raise ValueError(request.POST)
        for o in options:
            o_label = 'O' + str(o.pk)
            if (o_label in request.POST) != o.status:
                correct = False
        if correct:
            score.value = min(100, score.value+10)
            messages.add_message(request, messages.SUCCESS, 'Risposta esatta!')
        else:
            score.value = max(0, score.value-20)
            messages.add_message(request, messages.ERROR, 'Risposta sbagliata.')
    elif request.session['question_type']=='boolean':
        question = QuestionBoolean.objects.get(pk=request.session['question_pk'])
        if ('OTrue' in request.POST) == question.status:
            score.value = min(100, score.value+10)
            messages.add_message(request, messages.SUCCESS, 'Risposta esatta!')
        else:
            score.value = max(0, score.value-20)
            messages.add_message(request, messages.ERROR, 'Risposta sbagliata.')
    elif request.session['question_type']=='open':
        question = QuestionOpen.objects.get(pk=request.session['question_pk'])
        options = question.options.all()
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