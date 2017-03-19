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
        return render(request, 'backend/bloomer_detail.html', {'bloomer':bloomer, 'classrooms':classrooms})
    elif request.method == 'POST':
        bloomer.first_name = request.POST['first_name']
        bloomer.last_name = request.POST['last_name']
        bloomer.email = request.POST['email']
        bloomer.professor = 'professor' in request.POST
        bloomer.save()
        bloomer.update_classrooms([ key[-4:] for key in request.POST.keys() if key[:19]=='classroom_checkbox_' ])
        return render(request, 'backend/bloomer_detail.html', {'bloomer':bloomer, 'classrooms':classrooms})

def classrooms(request):
    return render(request, 'backend/classrooms.html', {'classrooms':blooming.Classroom.objects.all()})

def classroom_details(request, serial):
    classroom = blooming.Classroom.objects.get(serial=serial)
    if request.method == 'GET':
        return render(request, 'backend/classroom_detail.html', {'classroom':classroom})
    elif request.method == 'POST':
        pass

def topics_info(request):
    info = [ { 'serial':t.serial,
               'topic':t,
               'classrooms':( tc.classroom for tc in TopicClassroom.objects.filter(topic=t)),
               'antes':( td.ante for td in TopicDependency.objects.filter(post=t)),
               'posts':( td.post for td in TopicDependency.objects.filter(ante=t)),
               'questions': len(tuple(QuestionBoolean.objects.filter(topic=t))+
                            tuple(QuestionMultiple.objects.filter(topic=t))+
                            tuple(QuestionOpen.objects.filter(topic=t)))
              } for t in Topic.objects.all() ]
    return render(request, 'backend/topics_info.html', {'info':info})

def topic_questions(request, topic_serial):
    t = Topic.objects.get(serial=topic_serial)
    questions = tuple(QuestionBoolean.objects.filter(topic=t))+tuple(QuestionMultiple.objects.filter(topic=t))+tuple(QuestionOpen.objects.filter(topic=t))
    return render(request, 'backend/topic_questions.html', {'topic':t, 'questions':questions})