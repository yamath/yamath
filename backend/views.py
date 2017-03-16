from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from yapp.models import Classroom, ClassroomUser, Topic, Score, TopicClassroom, TopicDependency, Option, QuestionMultiple, QuestionBoolean, QuestionOpen, Claim

@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'backend/index.html')

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