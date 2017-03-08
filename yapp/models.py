from django.db import models
from django.contrib.auth.models import User

class Classroom(models.Model):
    serial = models.CharField(max_length=4)

    def __str__(self):
        return "(C %s)" % self.serial

class ClassroomUser(models.Model):
    user = models.ForeignKey(User, related_name="CU_user")
    classroom = models.ForeignKey('Classroom', related_name="CU_classroom")

    def __str__(self):
        return "(CU %s in %s)" % (self.user.username, self.classroom.serial)

class Topic(models.Model):
    serial = models.CharField(max_length=4)
    description = models.CharField(max_length=80)

    def __str__(self):
        return "(T%s %s)" % (self.serial, self.description)

class Score(models.Model):
    user = models.ForeignKey(User, related_name="S_user")
    topic = models.ForeignKey('Topic')
    value = models.IntegerField(default = 0)

    def __str__(self):
        return "(S %s has %s in %s)" % (self.user.username, self.value, self.topic.serial)

class TopicClassroom(models.Model):
    topic = models.ForeignKey('Topic', related_name="TC_topic")
    classroom = models.ForeignKey('Classroom', related_name="TC_classroom")

    def __str__(self):
        return "(TC %s for %s)" % (self.topic.serial, self.classroom.serial)

class TopicDependency(models.Model):
    ante = models.ForeignKey('Topic', related_name='TD_ante')
    post = models.ForeignKey('Topic', related_name='TD_post')

    def __str__(self):
        return "(TD %s before %s)" % (self.ante.serial, self.post.serial)

class Option(models.Model):
    text = models.TextField()
    status = models.BooleanField(default = False)

    def __str__(self):
        return "(O%s %s)" % (self.status, self.text)

class QuestionMultiple(models.Model):
    topic = models.ForeignKey('Topic', related_name='QM_topic')
    text = models.TextField()
    options = models.ManyToManyField('Option')
    notes = models.TextField(default="Seleziona tutte le risposte corrette e poi premi invia.")

    def __str__(self):
        return "(QM%s %s)" % (self.pk, self.text)

class QuestionBoolean(models.Model):
    topic = models.ForeignKey('Topic', related_name='QB_topic')
    text = models.TextField()
    status = models.BooleanField()
    notes = models.TextField(default="")

    def __str__(self):
        return "(QB%s %s)" % (self.pk, self.text)

class QuestionOpen(models.Model):
    topic = models.ForeignKey('Topic', related_name='QO_topic')
    text = models.TextField()
    options = models.ManyToManyField('Option')
    notes = models.TextField(default="Inserisci la risposta corretta e poi premi invia.")

    def __str__(self):
        return "(QO%d %s)" % (self.pk, self.text)
