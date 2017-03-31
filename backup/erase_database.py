from django.contrib.auth.models import User
#from blooming.models import *
#from backend.models import *

# User.objects.all().delete()
# Bloomer.objects.all().delete()
# Classroom.objects.all().delete()
# ClassroomBloomer.objects.all().delete()
# Topic.objects.all().delete()
# TopicDependency.objects.all().delete()
# TopicClassroom.objects.all().delete()
# Question.objects.all().delete()
# Option.objects.all().delete()
# Score.objects.all().delete()

import content.models as content

content.Serie.objects.all().delete()
content.SerieSerie.objects.all().delete()
content.Topic.objects.all().delete()
content.Question.objects.all().delete()
content.Option.objects.all().delete()