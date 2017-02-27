from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
  serial = models.CharField(max_length=4)
  description = models.CharField(max_length=40)
  content = models.TextField(default="This topic is not ready yet.")

  def __str__(self):
    return "%s (T%s)" % (self.description, self.serial)


class TopicDependency(models.Model):
  ante = models.ForeignKey('Topic', related_name='ante')
  post = models.ForeignKey('Topic', related_name='post')
  
  def __str__(self):
    return "TD(%s before %s)" % (self.ante.serial, self.post.serial)


class Question(models.Model):
  text = models.TextField(default="Question is not ready yet.")
  topic = models.ForeignKey('Topic', related_name='topic')
  notes =models.TextField(default="No notes on possible solutions.")

  def __str__(self):
    if len(self.text)>38:
      return "(Q%d) %s..." % (self.pk, self.text[:37])
    else:
      return "(Q%d) %s" % (self.pk, self.text)


class Answer(models.Model):
  question = models.ForeignKey('Question', related_name='question')
  answer = models.CharField(max_length=40)
  status = models.CharField(max_length=2)

  def __str__(self):
    if len(self.answer)>20:
      return "%s %s (%s...)" % (self.question.pk, self.status, self.answer[:17])
    else:
      return "%s %s (%s)" % (self.question.pk, self.status, self.answer)


class Score(models.Model):
  user = models.ForeignKey(User)
  topic = models.ForeignKey('Topic')
  value = models.IntegerField()

  def __str__(self):
    return "%s %s: %s" % (self.user.username, self.topic.pk, self.value)
