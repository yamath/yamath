import yapp.models as yapp
import blooming.models as blooming
from django.contrib.auth.models import User

blooming.Bloomer.objects.all().delete()
blooming.Classroom.objects.all().delete()
blooming.ClassroomBloomer.objects.all().delete()

for u in User.objects.all():
    blooming.Bloomer(user=u).save()

for c in yapp.Classroom.objects.all():
    blooming.Classroom(serial=c.serial).save()

for cu in yapp.ClassroomUser.objects.all():
    blooming.ClassroomBloomer(bloomer=blooming.Bloomer.objects.get(user=cu.user),
                              classroom=blooming.Classroom.objects.get(serial=cu.classroom.serial)).save()

