from django.contrib.auth.models import User
from blooming.models import *
from backend.models import *

User.objects.all().delete()
Bloomer.objects.all().delete()
Classroom.objects.all().delete()
ClassroomBloomer.objects.all().delete()
Topic.objects.all().delete()
TopicDependency.objects.all().delete()
TopicClassroom.objects.all().delete()
Question.objects.all().delete()
Option.objects.all().delete()
Score.objects.all().delete()
