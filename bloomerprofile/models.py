from django.db import models
from django.contrib.auth.models import User
from content.models import *
from question.models import *
from random import shuffle

class Bloomer(models.Model):
    class Meta:
        proxy = True

    def __repr__(self):
        return self.user.username

    def _get_classrooms(self):
        return [ cb.classroom for cb in ClassroomBloomer.objects.filter(bloomer=self) ]

    def _get_score_mean(self):
        return sum( self.get_scorevalue_of(t) for t in self.topics )/len(self.topics)

    def _get_topics(self):
        return list({ topic for classroom in self.classrooms for topic in classroom.topics })

    def get_scorevalue_of(self, topic):
        try:
            return Score.objects.get(user=self.user, topic=topic).value
        except:
            return 0

    def add_scorevalue_of(self, topic, i):
        try:
            score = Score.objects.get(user=self.user, topic=topic)
        except:
            score = Score(user=self.user, topic=topic, value=0)
        score.value = min(100, max(0, score.value+i))
        score.save()

    def update_classrooms(self, classrooms_serial_list):
        classrooms_to_add = set(classrooms_serial_list) - set([ c.serial for c in self.classrooms ])
        classrooms_to_delete = set([ c.serial for c in self.classrooms ]) - set(classrooms_serial_list)
        for serial in classrooms_to_add:
            ClassroomBloomer(bloomer=self, classroom=Classroom.objects.get(serial=serial)).save()
        for serial in classrooms_to_delete:
            ClassroomBloomer.objects.get(bloomer=self, classroom=Classroom.objects.get(serial=serial)).delete()


    classrooms = property(_get_classrooms)
    topics = property(_get_topics)
    score_mean = property(_get_score_mean)

class Classroom(models.Model):
    serial = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.serial

    def _get_bloomers(self):
        return [ cb.bloomer for cb in ClassroomBloomer.objects.filter(classroom=self) ]

    def _get_topics(self):
        return list({ tc.topic for tc in TopicClassroom.objects.filter(classroom=self) })

    def add_bloomer(self, bloomer):
        if bloomer not in self.bloomers:
            ClassroomBloomer(bloomer=bloomer, classroom=self).save()

    def del_bloomer(self, bloomer):
        if bloomer in self.bloomers:
            ClassroomBloomer.objects.get(bloomer=bloomer, classroom=self).delete()

    def add_topic(self, topic):
        if topic not in self.topics:
            TopicClassroom(topic=topic, classroom=self).save()

    def del_topic(self, topic):
        if topic in self.topics:
            TopicClassroom.objects.get(topic=topic, classroom=self).delete()

    bloomers = property(_get_bloomers)
    topics = property(_get_topics)

class ClassroomBloomer(models.Model):
    bloomer = models.ForeignKey('Bloomer', related_name="classroombloomer_bloomer")
    classroom = models.ForeignKey('Classroom', related_name="classroombloomer_classroom")

    def __str__(self):
        return "%s in %s" % (self.bloomer, self.classroom)