import yapp.models as yapp
import blooming.models as blooming
from django.contrib.auth.models import User

blooming.Bloomer.objects.all().delete()
blooming.Classroom.objects.all().delete()
blooming.ClassroomBloomer.objects.all().delete()
blooming.Topic.objects.all().delete()
blooming.TopicDependency.objects.all().delete()
blooming.TopicClassroom.objects.all().delete()

for u in User.objects.all():
    blooming.Bloomer(user=u).save()

for c in yapp.Classroom.objects.all():
    blooming.Classroom(serial=c.serial).save()

for cu in yapp.ClassroomUser.objects.all():
    blooming.ClassroomBloomer(bloomer=blooming.Bloomer.objects.get(user=cu.user),
                              classroom=blooming.Classroom.objects.get(serial=cu.classroom.serial)).save()

for t in yapp.Topic.objects.all():
    blooming.Topic(text=t.description).save()

for td in yapp.TopicDependency.objects.all():
    blooming.TopicDependency(ante=blooming.Topic.objects.get(text=td.ante.description),
                             post=blooming.Topic.objects.get(text=td.post.description)).save()

for tc in yapp.TopicClassroom.objects.all():
    blooming.TopicClassroom(topic=blooming.Topic.objects.get(text=tc.topic.description),
                            classroom=blooming.Classroom.objects.get(serial=tc.classroom.serial)).save()

