from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_user_is_professor(user):
    try:
        if isinstance(user, str):
            user = User.objects.get(username=user)
        assert UserInfo.objects.get(user=user).professor
    except:
        raise ValidationError

class Classroom(models.Model):
    serial = models.CharField(max_length=8, unique=True)
    _topics = models.ManyToManyField('Topic', related_name='classroom_topic')

    def __get_students(self):
        return list(Info.objects.filter(classroom=self, professor=False).select_related('user'))

    def __get_professors(self):
        return list(Info.objects.filter(classroom=self, professor=True).select_related('user'))

    def __get_topics(self):
        return list(self._topics.all())

    students = property(__get_students)
    professors = property(__get_professors)
    topics = property(__get_topics)

class Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    professor = models.BooleanField(default=False)
    _classrooms = models.ManyToManyField('Classroom', related_name="info_classroom", blank=True)

    def __get_classrooms(self):
        return list(self._classrooms.all())

    def __get_topics(self):
        return [ topic.serial for classroom in self.classrooms for topic in classroom.topics ]

    classrooms = property(__get_classrooms)
    topics = property(__get_topics)

class Topic(models.Model):
    text = models.CharField(max_length=40)
    bloom_index = models.IntegerField(  blank=True, null=True,
                                        choices=(   (1, 'remembering'),
                                                    (2, 'understanding'),
                                                    (3, 'applying'),
                                                    (4, 'analyzing'),
                                                    (5, 'evaluating'),
                                                    (6, 'creating'), ))
    mobile = models.BooleanField(default=False)
    _antes = models.ManyToManyField('Topic', blank=True)

    def __get_classrooms(self):
        return list(Classroom.objects.filter(_topics=self))

    def __get_students(self):
        return [ user for user in classroom.students for classroom in Classroom.objects.filter(_topic=self) ]

    def __get_professors(self):
        return [ user for user in classroom.professors for classroom in Classroom.objects.filter(_topic=self) ]

    def __get_questions(self):
        return list(Question.objects.filter(topic=self))

    classrooms = property(__get_classrooms)
    students = property(__get_students)
    professors = property(__get_professors)

    #def __str__(self):
    #    return "%s (T%s)" % (self.description, self.serial)

class Option(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    question = models.ForeignKey('Question', related_name="option_question")
    text = models.TextField()
    status = models.CharField(max_length=1, choices=(   ('a', 'accepted'),
                                                        ('p', 'pending'),
                                                        ('r', 'rejected') ))
    submit_time = models.DateTimeField(auto_now_add=True)
    interval = models.DurationField(blank=True, null=True)

class Question(models.Model):
    text = models.TextField()
    topic = models.ForeignKey('Topic', related_name='question_topic')
    note = models.TextField(blank=True, null=True)
    kind = models.CharField(max_length=8, choices=( ('ibool', 'instant boolean'),
                                                    ('imulti', 'instant multiple'),
                                                    ('iopen', 'instant open'),
                                                    ('pbool', 'paperwork boolean'),
                                                    ('pmulti', 'paperwork multiple'),
                                                    ('popen', 'paperwork open'),
                                                    ('delay', 'delayed'),
                                                    ('eval', 'evaluation')))

    def __get_options(self):
        return list(Option.objects.filter(question=self))

    options = property(__get_options)

class Score(models.Model):
    user = models.ForeignKey(User, related_name='score_user')
    topic = models.ForeignKey('Topic', related_name='score_topic')
    value = models.IntegerField()

    def __str__(self):
        return "%s %s: %s" % (self.user.username, self.topic.pk, self.value)

class Collection(models.Model):
    _topics = models.ManyToManyField('Topic')