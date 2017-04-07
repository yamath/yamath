from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
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
def classrooms(request):
    return render(request, 'backend/classrooms.html', {'classrooms':Classroom.objects.all()})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def classroom_details(request, serial):
    classroom = Classroom.objects.get(serial=serial)
    if request.method == 'GET':
        return render(request, 'backend/classroom_details.html', {'classroom':classroom})
    elif request.method == 'POST':
        #classroom.update_bloomers([ key[17:] for key in request.POST.keys() if key[:17]=='bloomer_checkbox_' ] + [request.POST['new_bloomer']])
        classroom.serial = request.POST['serial']
        if request.POST['add_topic']:
            classroom.add_topic(Topic.objects.get(pk=int(request.POST['add_topic'])))
        if request.POST['add_bloomer']:
            classroom.add_bloomer(Bloomer.objects.get(user=User.objects.get(request.POST['add_bloomer'])))
        if request.POST['delete_topic']:
            classroom.delete_topic(Topic.objects.get(pk=int(request.POST['delete_topic'])))
        if request.POST['delete_bloomer']:
            classroom.delete_bloomer(Bloomer.objects.get(user=User.objects.get(request.POST['delete_bloomer'])))
        classroom.save()
        return render(request, 'backend/classroom_details.html', {'classroom':classroom})


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
def question_details(request, question_pk):
    if (question_pk==None or question_pk=='None'):
        question_pk = request.GET['question_pk']
    question = Question.objects.get(pk=question_pk)
    if request.method == 'GET':
        return render(request, 'backend/question_details.html', {'question':question})
    elif request.method == 'POST':
        question.topic = Topic.objects.get(pk=request.POST['topic_pk'])
        question.text = request.POST['question_text']
        question.kind = request.POST['question_kind']
        for (key, value) in request.POST.items():
            if key[:11]=='option_text':
                option = Option.objects.get(pk=int(key[11:]))
                if value=='':
                    option.delete()
                else:
                    option.text = value
                    option.status = 'a' if ('option_accepted'+key[11:] in request.POST) else 'r'
                    option.save()
        if request.POST['new_option_text'] != '':
            new_option = Option(question=question, user=request.user, text=request.POST['new_option_text'], status=('a' if ('new_option_accepted' in request.POST) else 'r'))
            new_option.save()
        question.save()
        return render(request, 'backend/question_details.html', {'question':question})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def topics(request):
    return render(request, 'backend/topics.html', {'topics':Topic.objects.all()})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def topic_details(request, pk):
    topic = Topic.objects.get(pk=pk)
    classrooms = Classroom.objects.all()
    questions = Question.objects.filter(topic=topic)
    if request.method == 'GET':
        return render(request, 'backend/topic_details.html', {'topic':topic, 'classrooms':classrooms, 'questions':questions})
    elif request.method == 'POST':
        topic.update_antes([ key[15:] for key in request.POST.keys() if key[:15]=='antes_checkbox_' ] + [request.POST['new_ante']])
        topic.update_posts([ key[15:] for key in request.POST.keys() if key[:15]=='posts_checkbox_' ] + [request.POST['new_post']])
        topic.update_classrooms([ key[19:] for key in request.POST.keys() if key[:19]=='classroom_checkbox_' ])
        topic.text = request.POST['text']
        try:
            topic.bloom_index = int(request.POST['bloom_index'])
        except:
            topic.bloom_index = None
        topic.mobile = 'mobile' in request.POST
        topic.save()
        return render(request, 'backend/topic_details.html', {'topic':topic, 'classrooms':classrooms, 'questions':questions})
