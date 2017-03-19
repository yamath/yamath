from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
import yapp.models as yapp
import blooming.models as blooming

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
        topic.bloom_index = request.POST['bloom_index']
        topic.mobile = 'mobile' in request.POST
        topic.save()
        return render(request, 'backend/topic_details.html', {'topic':topic, 'classrooms':classrooms})
