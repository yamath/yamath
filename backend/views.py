from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
import blooming.models as blooming
import backend.models as backend
from django.contrib import messages

@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'backend/index.html')

def bloomers(request):
    return render(request, 'backend/bloomers.html', {'bloomers':blooming.Bloomer.objects.all()})

def bloomer_details(request, username):
    bloomer = blooming.Bloomer.objects.get(user=User.objects.get(username=username))
    classrooms = blooming.Classroom.objects.all()
    if request.method == 'GET':
        return render(request, 'backend/bloomer_details.html', {'bloomer':bloomer, 'classrooms':classrooms})
    elif request.method == 'POST':
        bloomer.first_name = request.POST['first_name']
        bloomer.last_name = request.POST['last_name']
        bloomer.email = request.POST['email']
        bloomer.professor = 'professor' in request.POST
        bloomer.save()
        bloomer.update_classrooms([ key[-4:] for key in request.POST.keys() if key[:19]=='classroom_checkbox_' ])
        return render(request, 'backend/bloomer_details.html', {'bloomer':bloomer, 'classrooms':classrooms})

def claim(request):
    try:
        bloomer = blooming.Bloomer.objects.get(pk=request.POST['claim_bloomer_pk'])
    except:
        bloomer = None
    try:
        topic = blooming.Topic.objects.get(pk=request.POST['claim_topic_pk'])
    except:
        topic = None
    try:
        question = blooming.Question.objects.get(pk=request.POST['claim_question_pk'])
    except:
        question = None
    try:
        option = blooming.Option.objects.get(pk=request.POST['claim_option_pk'])
    except:
        option = None
    backend.Claim(bloomer=bloomer, topic=topic, question=question, option=option).save()
    messages.info(request, "Grazie per il contributo.")
    return redirect('blooming:index')

def classrooms(request):
    return render(request, 'backend/classrooms.html', {'classrooms':blooming.Classroom.objects.all()})

def classroom_details(request, serial):
    classroom = blooming.Classroom.objects.get(serial=serial)
    if request.method == 'GET':
        return render(request, 'backend/classroom_details.html', {'classroom':classroom})
    elif request.method == 'POST':
        classroom.update_bloomers([ key[17:] for key in request.POST.keys() if key[:17]=='bloomer_checkbox_' ] + [request.POST['new_bloomer']])
        classroom.serial = request.POST['serial']
        classroom.save()
        return render(request, 'backend/classroom_details.html', {'classroom':classroom})

def pendings(request):
    return render(request, 'backend/pendings.html', {'pendings':blooming.Option.objects.filter(status='p')})

def pending_details(request, option_pk):
    option = blooming.Option.objects.get(pk=option_pk)
    other_options = blooming.Option.objects.filter(question=option.question, text=option.text)
    other_accepted = any( o.status == 'a' for o in other_options )
    other_rejected = any( o.status == 'r' for o in other_options )
    correct_answers = list({o.text for o in blooming.Option.objects.filter(question=option.question, status='a')})
    if request.method == 'GET':
        return render(request, 'backend/pending_details.html', {'option':option, 'correct_answers':correct_answers, 'other_accepted':other_accepted, 'other_rejected':other_rejected})
    elif request.method == 'POST':
        status = request.POST['status']
        for o in other_options:
            o.status = status
            o.save()
        return render(request, 'backend/pending_details.html', {'option':option, 'correct_answers':correct_answers, 'other_accepted':other_accepted, 'other_rejected':other_rejected})



def topics(request):
    return render(request, 'backend/topics.html', {'topics':blooming.Topic.objects.all()})

def topic_details(request, pk):
    topic = blooming.Topic.objects.get(pk=pk)
    classrooms = blooming.Classroom.objects.all()
    if request.method == 'GET':
        return render(request, 'backend/topic_details.html', {'topic':topic, 'classrooms':classrooms})
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
        return render(request, 'backend/topic_details.html', {'topic':topic, 'classrooms':classrooms})
