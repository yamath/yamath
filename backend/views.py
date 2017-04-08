from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.views.decorators.cache import never_cache
from bloomerprofile.models import *
from content.models import *
import backend.models as backend
from django.contrib import messages
from backend.create_views import *

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def index(request):
    bloomers = sorted(Bloomer.objects.all(), key=(lambda bloomer: bloomer.mean))
    classrooms = Classroom.objects.all()
    series = Serie.objects.all()
    return render(request, 'backend/index.html', {'bloomers':bloomers, 'classrooms':classrooms, 'series':series})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def bloomers(request):
    return render(request, 'backend/bloomers.html', {'bloomers':Bloomer.objects.all(), 'classrooms':Classroom.objects.all()})

@never_cache
def bloomer_details(request, username):
    if not (request.user.is_superuser or request.user.username == username):
        return redirect('/')
    bloomer = Bloomer.objects.get(username=username)
    classrooms = Classroom.objects.all()
    if request.method == 'GET':
        return render(request, 'backend/bloomer_details.html', {'bloomer':bloomer, 'classrooms':classrooms})
    elif request.method == 'POST':
        bloomer.first_name = request.POST['first_name']
        bloomer.last_name = request.POST['last_name']
        bloomer.email = request.POST['email']
        if 'password' in request.POST and len(request.POST['password'])>4:
            bloomer.set_password(request.POST['password'])
        bloomer.save()
        return render(request, 'backend/bloomer_details.html', {'bloomer':bloomer, 'classrooms':classrooms})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def classrooms(request):
    return render(request, 'backend/classrooms.html', {'classrooms':Classroom.objects.all()})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def classroom_details(request, name):
    classroom = Classroom.objects.get(name=name)
    if request.method == 'GET':
        return render(request, 'backend/classroom_details.html', {'classroom':classroom})
    elif request.method == 'POST':
        classroom.name = request.POST['name']
        if request.POST['add_serie']:
            classroom.add_serie(Serie.objects.get(serial=request.POST['add_serie']))
        if request.POST['add_bloomer']:
            classroom.add_bloomer(Bloomer.objects.get(username=request.POST['add_bloomer']))
        if request.POST['del_serie']:
            classroom.del_serie(Serie.objects.get(serial=request.POST['del_serie']))
        if request.POST['del_bloomer']:
            classroom.del_bloomer(Bloomer.objects.get(username=request.POST['del_bloomer']))
        classroom.save()
        return render(request, 'backend/classroom_details.html', {'classroom':classroom})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def series(request):
    series = Serie.objects.all()
    return render(request, 'backend/series.html', {'series':series})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def serie_new(request):
    if request.method == 'GET':
        return render(request, 'backend/serie_new.html')
    elif request.method == 'POST':
        serie = Serie.objects.create(serial='0', name='N/N')
        serie.name = request.POST['name']
        serials = { int(s.serial) for s in Serie.objects.all() }
        serie.serial = "{0:03d}".format(min( set(range(1, max(serials)+2)) - serials ))
        serie.save()
        return redirect(reverse('backend:serie_details', args=(serie.serial,)))
        return render(request, 'backend/serie_details.html', {'serie':serie})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def serie_details(request, serieSerial):
    serie = Serie.objects.get(serial=serieSerial)
    if request.method == 'GET':
        return render(request, 'backend/serie_details.html', {'serie':serie})
    elif request.method == 'POST':
        serie.name = request.POST['name']
        if 'add_ante' in request.POST and len(request.POST['add_ante'])>0:
            serie.add_ante(request.POST['add_ante'])
        if 'del_ante' in request.POST and len(request.POST['del_ante'])>0:
            serie.del_ante(request.POST['del_ante'])
        serie.save()
        return render(request, 'backend/serie_details.html', {'serie':serie})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def topic_new(request, serieSerial):
    if request.method == 'GET':
        serie = Serie.objects.get(serial=serieSerial)
        serials = {0}.union({ int(t.serial[-3:]) for t in Topic.objects.filter(serie=serie) })
        serial = "{0}{1:03d}".format(serie.serial, min( set(range(1, max(serials)+2)) - serials ))
        topic = Topic.objects.create(serial=serial, name='name', serie=serie)
        topic.save()
        return redirect(reverse('backend:topic_details', args=(topic.serial,)))

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def topic_details(request, topicSerial):
    topic = Topic.objects.get(serial = topicSerial)
    if request.method == 'GET':
        return render(request, 'backend/topic_details.html', {'topic':topic})
    elif request.method == 'POST':
        topic.name = request.POST['name']
        topic.mobile = 'mobile' in request.POST
        try:
            topic.kind = int(request.POST['kind'])
        except:
            pass
        topic.save()
        return render(request, 'backend/topic_details.html', {'topic':topic})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def question_new(request, topicSerial):
    if request.method == 'GET':
        topic = Topic.objects.get(serial=topicSerial)
        serials = {0}.union({ int(q.serial[-3:]) for q in Question.objects.filter(topic=topic) })
        serial = "{0}{1:03d}".format(topic.serial, min( set(range(1, max(serials)+2)) - serials ))
        question = Question.objects.create(serial=serial, text='text', topic=topic, kind='o')
        question.save()
        return redirect(reverse('backend:question_details', args=(question.serial,)))

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def question_details(request, questionSerial):
    question = Question.objects.get(serial = questionSerial)
    if request.method == 'GET':
        return render(request, 'backend/question_details.html', {'question':question})
    elif request.method == 'POST':
        question.text = request.POST['text']
        question.kind = request.POST['kind']
        question.save()
        return render(request, 'backend/question_details.html', {'question':question})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def option_new(request, questionSerial):
    if request.method == 'GET':
        question = Question.objects.get(serial=questionSerial)
        serials = {0}.union({ int(q.serial[-3:]) for q in Option.objects.filter(question=question) })
        serial = "{0}{1:03d}".format(question.serial, min( set(range(1, max(serials)+2)) - serials ))
        option = Option.objects.create(serial=serial, text='text', question=question)
        option.save()
        return redirect(reverse('backend:option_details', args=(option.serial,)))

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def option_details(request, optionSerial):
    option = Option.objects.get(serial = optionSerial)
    if request.method == 'GET':
        return render(request, 'backend/option_details.html', {'option':option})
    elif request.method == 'POST':
        option.text = request.POST['text']
        option.accepted = 'accepted' in request.POST
        option.save()
        return render(request, 'backend/option_details.html', {'option':option})
    
    
    
    
def claim(request):
    try:
        bloomer = Bloomer.objects.get(pk=request.POST['claim_bloomer_pk'])
    except:
        bloomer = None
    try:
        topic = Topic.objects.get(pk=request.POST['claim_topic_pk'])
    except:
        topic = None
    try:
        question = Question.objects.get(pk=request.POST['claim_question_pk'])
    except:
        question = None
    try:
        option = Option.objects.get(pk=request.POST['claim_option_pk'])
    except:
        option = None
    backend.Claim(bloomer=bloomer, topic=topic, question=question, option=option).save()
    messages.info(request, "Grazie per il contributo.")
    return redirect('blooming:index')

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def claim_solved(request, claim_pk):
    backend.Claim.objects.get(pk=claim_pk).delete()
    return redirect('backend:claims')

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def claims(request):
    return render(request, 'backend/claims.html', {'claims':backend.Claim.objects.all()})


@never_cache
@user_passes_test(lambda u: u.is_superuser)
def new_question(request):
    if request.method == 'GET':
        return render(request, 'backend/new_question.html', {'question':None})
    elif request.method == 'POST':
        question = Question(topic=Topic.objects.get(pk=request.POST['topic_pk']),
                                     text=request.POST['question_text'],
                                     kind=request.POST['question_kind'])
        question.save()
        for (key, value) in request.POST.items():
            if key[:11]=='option_text':
                option = Option.objects.get(pk=int(key[11:]))
                if value=='':
                    option.delete()
                else:
                    option.text = value
                    option.status = 'a' if ('option_accepted'+key[11:] in request.POST) else 'r'
                    option.save()
        if 'new_option_text' in request.POST and request.POST['new_option_text'] != '':
            new_option = Option(question=question, user=request.user, text=request.POST['new_option_text'], status=('a' if ('new_option_accepted' in request.POST) else 'r'))
            new_option.save()
        return render(request, 'backend/question_details.html', {'question':question})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def pendings(request):
    return render(request, 'backend/pendings.html', {'pendings':Option.objects.filter(status='p')})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def pending_details(request, option_pk):
    option = Option.objects.get(pk=option_pk)
    other_options = Option.objects.filter(question=option.question, text=option.text)
    other_accepted = any( o.status == 'a' for o in other_options )
    other_rejected = any( o.status == 'r' for o in other_options )
    correct_answers = list({o.text for o in Option.objects.filter(question=option.question, status='a')})
    if request.method == 'GET':
        return render(request, 'backend/pending_details.html', {'option':option, 'correct_answers':correct_answers, 'other_accepted':other_accepted, 'other_rejected':other_rejected})
    elif request.method == 'POST':
        status = request.POST['status']
        for o in other_options:
            o.status = status
            o.save()
        return render(request, 'backend/pending_details.html', {'option':option, 'correct_answers':correct_answers, 'other_accepted':other_accepted, 'other_rejected':other_rejected})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def pending_solved(request, option_pk):
    option = Option.objects.get(pk=option_pk)
    if 'option_accepted' in request.POST:
        option.status = 'a'
    elif 'option_rejected' in request.POST:
        option.status = 'r'
    else:
        raise ValueError
    option.save()
    return redirect('backend:pendings')


@never_cache
@user_passes_test(lambda u: u.is_superuser)
def topics(request):
    return render(request, 'backend/topics.html', {'topics':Topic.objects.all()})
