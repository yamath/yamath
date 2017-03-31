from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from random import shuffle
from content.models import Topic, Question, Option
#def validate_user_is_professor(user):
#    try:
#        if isinstance(user, str):
#            user = User.objects.get(username=user)
#        assert UserInfo.objects.get(user=user).professor
#    except:
#        raise ValidationError

class Bloomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    professor = models.BooleanField(default=False)

    def __str__(self):
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

    def delete_bloomer(self, bloomer):
        if bloomer in self.bloomers:
            ClassroomBloomer.objects.get(bloomer=bloomer, classroom=self).delete()

    def add_topic(self, topic):
        if topic not in self.topics:
            TopicClassroom(topic=topic, classroom=self).save()

    def delete_topic(self, topic):
        if topic in self.topics:
            TopicClassroom.objects.get(topic=topic, classroom=self).delete()
    #def update_bloomers(self, bloomers_username_list):
    #    bloomers_to_add = (set(bloomers_username_list) - set([ b.user.username for b in self.bloomers ])) & set([ b.user.username for b in Bloomer.objects.all() ])
    #    bloomers_to_delete = set([ b.user.username for b in self.bloomers ]) - set(bloomers_username_list)
    #    for username in bloomers_to_add:
    #        ClassroomBloomer(bloomer=Bloomer.objects.get(user=User.objects.get(username=username)), classroom=self).save()
    #    for username in bloomers_to_delete:
    #        ClassroomBloomer.objects.get(bloomer=Bloomer.objects.get(user=User.objects.get(username=username)), classroom=self).delete()

    bloomers = property(_get_bloomers)
    topics = property(_get_topics)

class ClassroomBloomer(models.Model):
    bloomer = models.ForeignKey(Bloomer, related_name="classroombloomer_bloomer")
    classroom = models.ForeignKey(Classroom, related_name="classroombloomer_classroom")

    def __str__(self):
        return "%s in %s" % (self.bloomer, self.classroom)

# class Topic(models.Model):
#     text = models.CharField(max_length=80)
#     bloom_index = models.IntegerField(  blank=True, null=True,
#                                         choices=(   (1, 'remembering'),
#                                                     (2, 'understanding'),
#                                                     (3, 'applying'),
#                                                     (4, 'analyzing'),
#                                                     (5, 'evaluating'),
#                                                     (6, 'creating'), ))
#     mobile = models.BooleanField(default=False)

#     def __str__(self):
#         return self.text

#     def update_antes(self, antes_pk_list):
#         for pk in antes_pk_list:
#             try:
#                 t = Topic.objects.get(pk=int(pk))
#                 if t not in self.antes:
#                     TopicDependency(ante=t, post=self).save()
#             except:
#                 pass
#         for t in self.antes:
#             if str(t.pk) not in antes_pk_list:
#                 TopicDependency.objects.get(ante=t, post=self).delete()

#     def update_posts(self, posts_pk_list):
#         for pk in posts_pk_list:
#             try:
#                 t = Topic.objects.get(pk=int(pk))
#                 if t not in self.posts:
#                     TopicDependency(ante=self, post=t).save()
#             except:
#                 pass
#         for t in self.posts:
#             if str(t.pk) not in posts_pk_list:
#                 TopicDependency.objects.get(ante=self, post=t).delete()

#     def update_classrooms(self, classrooms_serial_list):
#         classrooms_to_add = set(classrooms_serial_list) - set([ c.serial for c in self.classrooms ])
#         classrooms_to_delete = set([ c.serial for c in self.classrooms ]) - set(classrooms_serial_list)
#         for serial in classrooms_to_add:
#             TopicClassroom(topic=self, classroom=Classroom.objects.get(serial=serial)).save()
#         for serial in classrooms_to_delete:
#             TopicClassroom.objects.get(topic=self, classroom=Classroom.objects.get(serial=serial)).delete()

#     def _get_antes(self):
#         return list({ td.ante for td in TopicDependency.objects.filter(post=self) })

#     def _get_classrooms(self):
#         return list({ tc.classroom for tc in TopicClassroom.objects.filter(topic=self) })

#     def _get_posts(self):
#         return list({ td.post for td in TopicDependency.objects.filter(ante=self) })

#     def _get_questions(self):
#         return list(Question.objects.filter(topic=self))

#     antes = property(_get_antes)
#     classrooms = property(_get_classrooms)
#     posts = property(_get_posts)
#     questions = property(_get_questions)

# class TopicDependency(models.Model):
#     ante = models.ForeignKey('Topic', related_name='topicdependency_ante')
#     post = models.ForeignKey('Topic', related_name='topicdependency_post')

#     def __str__(self):
#         return "%s BEFORE %s" % (self.ante, self.post)

class TopicClassroom(models.Model):
    topic = models.ForeignKey(Topic, related_name='topicclassroom_topic')
    classroom = models.ForeignKey(Classroom, related_name='topicclassroom_classroom')

    def __str__(self):
        return "%s FOR %s" % (self.topic, self.classroom)

# class Option(models.Model):
#     user = models.ForeignKey(User, blank=True, null=True)
#     question = models.ForeignKey('Question', related_name="option_question")
#     text = models.TextField()
#     status = models.CharField(max_length=1, choices=(   ('a', 'accepted'),
#                                                         ('p', 'pending'),
#                                                         ('r', 'rejected') ))
#     submit_time = models.DateTimeField(auto_now_add=True)
#     interval = models.DurationField(blank=True, null=True)

#     def __str__(self):
#         return "%s %s: %s TO %s (%s)" % (self.user.username, self.submit_time, self.text, self.question.pk, self.status)

# class Question(models.Model):
#     text = models.TextField()
#     topic = models.ForeignKey('Topic', related_name='question_topic')
#     note = models.TextField(blank=True, null=True)
#     kind = models.CharField(max_length=8, choices=( ('ibool', 'instant boolean'),
#                                                     ('imulti', 'instant multiple'),
#                                                     ('iopen', 'instant open'),
#                                                     ('pbool', 'paperwork boolean'),
#                                                     ('pmulti', 'paperwork multiple'),
#                                                     ('popen', 'paperwork open'),
#                                                     ('delay', 'delayed'),
#                                                     ('eval', 'evaluation')))

#     def __str__(self):
#         return "(T%s %s %s) %s" % (self.topic.pk, self.kind, self.pk, self.text[:80])

#     def _get_options(self):
#         return list(Option.objects.filter(question=self))

#     def distinct_nonpending_options(self):
#         return [ Option.objects.filter(question=self, text=text).first() for text in { option.text for option in Option.objects.filter(question=self) if option.status != 'p' } ]

#     def get_correct(self):
#         try:
#             return Option.objects.filter(question=self, status='a').first()
#         except:
#             return None

#     def get_uptofive(self):
#         l =  [self.get_correct()] + [ Option.objects.filter(question=self, text=text).first() for text in { option.text for option in Option.objects.filter(question=self) if option.status == 'r' } ][:4]
#         shuffle(l)
#         return l

#     def get_status(self, answer):
#         equivalent_options = Option.objects.filter(question=self, text=answer)
#         if len(equivalent_options)>0:
#             if all( option.status == 'a' for option in equivalent_options ):
#                 status = 'a'
#             elif all( option.status == 'r' for option in equivalent_options ):
#                 status = 'r'
#             else:
#                 status = 'p'
#         elif self.kind in ['ibool', 'imulti', 'iopen', 'pbool', 'pmulti', 'popen']:
#             accepted_options = Option.objects.filter(question=self, status='a')
#             if answer in [ option.text for option in accepted_options ]:
#                 status = 'a'
#             else:
#                 status = 'r'
#         else:
#             status = 'p'
#         return status

#     def shuffled_options(self):
#         l = self.distinct_nonpending_options()
#         shuffle(l)
#         return l

#     options = property(_get_options)

class Score(models.Model):
    user = models.ForeignKey(User, related_name='score_user')
    topic = models.ForeignKey(Topic, related_name='score_topic')
    value = models.IntegerField()

    def __str__(self):
        return "%s %s: %s" % (self.user.username, self.topic.pk, self.value)