from django.db import models
from django.contrib.auth.models import User
from content.models import *
from random import choice, shuffle
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def get_or_none(_class, **kwargs):
    try:
        return _class.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None
    

class Bloomer(User):
    class Meta:
        proxy = True

    def __repr__(self):
        return self.username        

    def add_classroom(self, c):
        if isinstance(c, Classroom):
            classroom = c
        else:
            classroom = get_or_none(Classroom, name=c) or get_or_none(Classroom, pk=c)
        if classroom is not None and classroom not in self.classrooms:
            ClassroomBloomer(bloomer=self, classroom=classroom).save()

    def add_forget(self):
        choice(Mean.objects.filter(bloomer=self)).add_forget()

    def add_unanswered(self, t):
        if isinstance(t, Topic):
            topic = t
        else:
            topic = get_or_none(Topic, serial=t) or get_or_none(Topic, pk=t)
        try:
            Mean.objects.get(bloomer=self, topic=topic).add_unanswered()
        except ObjectDoesNotExist:
            m = Mean(bloomer=self, topic=topic)
            m.save()
            m.add_unanswered()

    def chk_answer(self, q, text):
        print("chk_answer", q.serial, text)
        if isinstance(q, Question):
            question = q
        else:
            question = get_or_none(Question, serial=q) or get_or_none(Question, pk=q)
        print("mean ante", self.get_mean_of_topic(question.topic))
        if question.chk_answer(text):
            try:
                Mean.objects.get(bloomer=self, topic=question.topic).add_accepted()
            except ObjectDoesNotExist:
                m = Mean(bloomer=self, topic=question.topic)
                m.save()
                m.add_accepted()
            print("mean post", self.get_mean_of_topic(question.topic))
            return True
        else:
            try:
                Mean.objects.get(bloomer=self, topic=question.topic).add_rejected()
            except ObjectDoesNotExist:
                m = Mean(bloomer=self, topic=question.topic)
                m.save()
                m.add_rejected()
            print("mean post", self.get_mean_of_topic(question.topic))
            return False

    def del_classroom(self, c):
        if isinstance(c, Classroom):
            classroom = c
        else:
            classroom = get_or_none(Classroom, name=c) or get_or_none(Classroom, pk=c)
        if classroom in self.classrooms:
            ClassroomBloomer.objects.get(bloomer=self, classroom=classroom).delete()

    def get_classrooms(self):
        return [ cb.classroom for cb in ClassroomBloomer.objects.filter(bloomer=self) ]

    def get_classrooms_of_serie(self, s):
        if isinstance(s, Serie):
            serie = s
        else:
            serie = get_or_none(Serie, serial=s)
        return [ sc.classroom for sc in SerieClassroom.objects.filter(serie=serie) ]

    def get_mean(self):
        series = self.series
        if len(series)==0:
            return 1
        return sum( self.get_mean_of_serie(s) for s in series )/len(series)

    def get_mean_of_topic(self, t):
        if isinstance(t, Topic):
            topic = t
        else:
            topic = get_or_none(Topic, serial=t) or get_or_none(Topic, pk=t)
        try:
            return Mean.objects.get(bloomer=self, topic=topic).mean
        except ObjectDoesNotExist:
            m = Mean(bloomer=self, topic=topic)
            m.save()
            return m.mean

    def get_mean_of_serie(self, s):
        if isinstance(s, Serie):
            serie = s
        else:
            serie = get_or_none(Serie, serial=s)
        topics = serie.topics
        if len(topics)==0:
            return 1
        return sum( self.get_mean_of_topic(t) for t in topics )/len(topics)

    def get_topics(self):
        return list({ topic for topic in serie.topics for serie in self.series })

    def get_series(self):
        return list({ serie for classroom in self.classrooms  for serie in classroom.series})


    classrooms = property(get_classrooms)
    series = property(get_series)
    topics = property(get_topics)
    mean = property(get_mean)


class Classroom(models.Model):
    name = models.CharField(max_length=4, unique=True)

    def __repr__(self):
        return self.name

    def get_bloomers(self):
        return [ cb.bloomer for cb in ClassroomBloomer.objects.filter(classroom=self) ]

    def get_series(self):
        return list({ sc.serie for sc in SerieClassroom.objects.filter(classroom=self) })

    def add_bloomer(self, b):
        if isinstance(b, Bloomer):
            bloomer = b
        else:
            bloomer = get_or_none(Bloomer, username=b) or get_or_none(Bloomer, pk=b)
        if bloomer not in self.bloomers:
            ClassroomBloomer(bloomer=bloomer, classroom=self).save()

    def add_serie(self, s):
        if isinstance(s, Serie):
            serie = s
        else:
            serie = get_or_none(Serie, serial=s)
        if serie not in self.series:
            SerieClassroom(classroom=self, serie=serie).save()

    def del_bloomer(self, b):
        if isinstance(b, Bloomer):
            bloomer = b
        else:
            bloomer = get_or_none(Bloomer, username=b) or get_or_none(Bloomer, pk=b)
        if bloomer in self.bloomers:
            ClassroomBloomer.objects.get(bloomer=bloomer, classroom=self).delete()

    def del_serie(self, s):
        if isinstance(s, Serie):
            serie = s
        else:
            serie = get_or_none(Serie, serial=s)
        if serie in self.series:
            SerieClassroom.objects.get(classroom=self, serie=serie).delete()

    bloomers = property(get_bloomers)
    series = property(get_series)


class ClassroomBloomer(models.Model):
    bloomer = models.ForeignKey(Bloomer, related_name="classroombloomer_bloomer")
    classroom = models.ForeignKey(Classroom, related_name="classroombloomer_classroom")

    def __str__(self):
        return "%s in %s" % (self.bloomer, self.classroom)


class SerieClassroom(models.Model):
    classroom = models.ForeignKey(Classroom, related_name="serieclassroom_classroom")
    serie = models.ForeignKey(Serie, related_name="serieclassroom_serie")

    def __str__(self):
        return "%s for %s" % (self.serie, self.classroom)


class Mean(models.Model):
    bloomer = models.ForeignKey(Bloomer, related_name="mean_bloomer")
    topic = models.ForeignKey(Topic, related_name="mean_topic")
    history = models.CharField(max_length=10, default='XXXXXXXXXX')
    forget = models.IntegerField(default=0)

    def __str__(self):
        return "%s in %s: %s" % (self.bloomer, repr(self.topic), self.history)

    def add_accepted(self):
        self.history = 'A' + self.history[:9]
        self.del_forget()

    def add_forget(self):
        self.forget += 1
        self.save()

    def add_rejected(self):
        self.history = 'R' + self.history[:9]
        self.save()

    def add_unanswered(self):
        self.history = 'X' + self.history[:9]
        self.save()

    def del_forget(self):
        self.forget = max(0, self.forget-1)
        self.save()

    def get_mean(self):
        return 0.9**self.forget * (
                10*(1 if self.history[0] == 'A' else 0)+
                 5*(1 if self.history[1] == 'A' or self.history[0] == 'X' else 0)+
                 2*(1 if self.history[2] == 'A' or self.history[1] == 'X' else 0)+
                 1*(1 if self.history[3] == 'A' or self.history[2] == 'X' else 0)
                )/18

    mean = property(get_mean)

    
class Envelope(models.Model):
    sender = models.ForeignKey(Bloomer, related_name="envelope_sender")
    receiver = models.ForeignKey(Bloomer, related_name="envelope_receiver")
    serie = models.ForeignKey(Serie, blank=True, null=True, related_name="envelope_serie")
    topic = models.ForeignKey(Topic, blank=True, null=True, related_name="envelope_topic")
    question = models.ForeignKey(Question, blank=True, null=True, related_name="envelope_question")
    option = models.ForeignKey(Option, blank=True, null=True, related_name="envelope_option")
    text = models.TextField(blank=True, null=True)
    submit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "from %s to %s" % (self.sender, self.receiver)