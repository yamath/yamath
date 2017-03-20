from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

    def _get_classrooms(self):
        return [ cb.classroom for cb in ClassroomBloomer.objects.filter(bloomer=self) ]

    def _get_topics(self):
        return None

    def update_classrooms(self, classrooms_serial_list):
        classrooms_to_add = set(classrooms_serial_list) - set([ c.serial for c in self.classrooms ])
        classrooms_to_delete = set([ c.serial for c in self.classrooms ]) - set(classrooms_serial_list)
        for serial in classrooms_to_add:
            ClassroomBloomer(bloomer=self, classroom=Classroom.objects.get(serial=serial)).save()
        for serial in classrooms_to_delete:
            ClassroomBloomer.objects.get(bloomer=self, classroom=Classroom.objects.get(serial=serial)).delete()


    classrooms = property(_get_classrooms)
    topics = property(_get_topics)

class Classroom(models.Model):
    serial = models.CharField(max_length=4, unique=True)

    def _get_bloomers(self):
        return [ cb.bloomer for cb in ClassroomBloomer.objects.filter(classroom=self) ]

    def _get_topics(self):
        return list({ tc.topic for tc in TopicClassroom.objects.filter(classroom=self) })

    def update_bloomers(self, bloomers_username_list):
        bloomers_to_add = (set(bloomers_username_list) - set([ b.user.username for b in self.bloomers ])) & set([ b.user.username for b in Bloomer.objects.all() ])
        bloomers_to_delete = set([ b.user.username for b in self.bloomers ]) - set(bloomers_username_list)
        for username in bloomers_to_add:
            ClassroomBloomer(bloomer=Bloomer.objects.get(user=User.objects.get(username=username)), classroom=self).save()
        for username in bloomers_to_delete:
            ClassroomBloomer.objects.get(bloomer=Bloomer.objects.get(user=User.objects.get(username=username)), classroom=self).delete()

    bloomers = property(_get_bloomers)
    topics = property(_get_topics)

class ClassroomBloomer(models.Model):
    bloomer = models.ForeignKey('Bloomer', related_name="classroombloomer_bloomer")
    classroom = models.ForeignKey('Classroom', related_name="classroombloomer_classroom")

class Topic(models.Model):
    text = models.CharField(max_length=80)
    bloom_index = models.IntegerField(  blank=True, null=True,
                                        choices=(   (1, 'remembering'),
                                                    (2, 'understanding'),
                                                    (3, 'applying'),
                                                    (4, 'analyzing'),
                                                    (5, 'evaluating'),
                                                    (6, 'creating'), ))
    mobile = models.BooleanField(default=False)

    def update_antes(self, antes_pk_list):
        for pk in antes_pk_list:
            try:
                t = Topic.objects.get(pk=int(pk))
                if t not in self.antes:
                    TopicDependency(ante=t, post=

    def update_posts(self, posts_pk_list):
        posts_to_add = (set(posts_pk_list) - set([ str(p.pk) for p in self.posts ])) & set([ str(t.pk) for t in Topic.objects.all() ])
        posts_to_delete = set([ str(p.pk) for p in self.posts ]) - set(posts_pk_list)
        for pk in posts_to_add:
            TopicDependency(ante=self, post=Topic.objects.get(pk=int(pk))).save()
        for pk in posts_to_delete:
            TopicDependency.objects.get(ante=self, post=Topic.objects.get(pk=int(pk))).delete()

    def update_classrooms(self, classrooms_serial_list):
        classrooms_to_add = set(classrooms_serial_list) - set([ c.serial for c in self.classrooms ])
        classrooms_to_delete = set([ c.serial for c in self.classrooms ]) - set(classrooms_serial_list)
        for serial in classrooms_to_add:
            TopicClassroom(topic=self, classroom=Classroom.objects.get(serial=serial)).save()
        for serial in classrooms_to_delete:
            TopicClassroom.objects.get(topic=self, classroom=Classroom.objects.get(serial=serial)).delete()

    def _get_antes(self):
        return list({ td.ante for td in TopicDependency.objects.filter(post=self) })

    def _get_classrooms(self):
        return list({ tc.classroom for tc in TopicClassroom.objects.filter(topic=self) })

    def _get_posts(self):
        return list({ td.post for td in TopicDependency.objects.filter(ante=self) })

    antes = property(_get_antes)
    posts = property(_get_posts)
    classrooms = property(_get_classrooms)

class TopicDependency(models.Model):
    ante = models.ForeignKey('Topic', related_name='topicdependency_ante')
    post = models.ForeignKey('Topic', related_name='topicdependency_post')

class TopicClassroom(models.Model):
    topic = models.ForeignKey('Topic', related_name='topicclassroom_topic')
    classroom = models.ForeignKey('Classroom', related_name='topicclassroom_classroom')

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