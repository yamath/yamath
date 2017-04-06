from django.db import models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from random import sample, shuffle

def get_or_none(_class, **kwargs):
    try:
        return _class.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None


class Serie(models.Model):
    serial = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=80)
    recollection = models.BooleanField(default=False)
    hindex = models.IntegerField(default=0)

    def __repr__(self):
        return "S%s" % self.serial

    def __str__(self):
        return self.name

    def add_ante(self, s):
        if isinstance(s, Serie):
            serie = s
        else:
            serie = get_or_none(Serie, serial=s)
        if serie is not None and serie not in self.antes:
            SerieSerie(ante=serie, post=self).save()

    def add_post(self, s):
        if isinstance(s, Serie):
            serie = s
        else:
            serie = get_or_none(Serie, serial=s)
        if serie not in self.posts:
            SerieSerie(ante=self, post=serie).save()

    def del_ante(self, s):
        if isinstance(s, Serie):
            serie = s
        else:
            serie = get_or_none(Serie, serial=s)
        if serie in self.antes:
            SerieSerie.objects.get(ante=serie, post=self).delete()

    def del_post(self, s):
        if isinstance(s, Serie):
            serie = s
        else:
            serie = get_or_none(Serie, serial=s)
        if serie in self.posts:
            SerieSerie.objects.get(ante=self, post=serie).delete()

    def get_antes(self):
        return list({ ss.ante for ss in SerieSerie.objects.filter(post=self) })

    def get_posts(self):
        return list({ ss.post for ss in SerieSerie.objects.filter(ante=self) })

    def get_topics(self):
        return list(Topic.objects.filter(serie=self))

    def set_hindex(self):
        if self.antes:
            self.hindex = max( s.hindex for s in self.antes ) + 1
        else:
            self.hindex = 1

    antes = property(get_antes)
    posts = property(get_posts)
    topics = property(get_topics)


class SerieSerie(models.Model):
    ante = models.ForeignKey('Serie', related_name='serieserie_ante')
    post = models.ForeignKey('Serie', related_name='serieserie_post')

    def __repr__(self):
        return "SS(%s < %s)" % (self.ante.serial, self.post.serial)


class Topic(models.Model):
    serial = models.CharField(max_length=6, unique=True)
    kind = models.IntegerField( blank=True, null=True,
                                choices=(   (1, 'remembering'),
                                            (2, 'understanding'),
                                            (3, 'applying'),
                                            (4, 'analyzing'),
                                            (5, 'evaluating'),
                                            (6, 'creating'), ))
    mobile = models.BooleanField(default=False)
    name = models.CharField(max_length=80)
    serie = models.ForeignKey('Serie', related_name="topic_serie")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "T%s" % (self.serial)

    def chk_serial(self):
        return self.serial[0:3] == self.serie.serial

    def get_questions(self):
        return list(Question.objects.filter(topic=self))

    questions = property(get_questions)


class Question(models.Model):
    serial = models.CharField(max_length=9, unique=True)
    text = models.TextField()
    topic = models.ForeignKey(Topic, related_name='question_topic')
    kind = models.CharField(max_length=1, choices=( ('b', 'True or false'),
                                                    ('m', 'Multiple choice'),
                                                    ('o', 'Open question'),
                                                    ('t', 'Teacher evaluated question'),
                                                    ('w', 'Work to deliver to the teacher')))

    def __str__(self):
        return "%s" % self.text

    def __repr__(self):
        return "Q%s%s" % (self.kind, self.serial)

    def chk_serial(self):
        return self.serial[0:6] == self.topic.serial
    
    def get_correct(self):
        return Option.objects.filter(question=self, accepted=True).first()

    def get_options(self):
        return list(Option.objects.filter(question=self))

    def get_uptofive(self):
        correct_option = Option.objects.filter(question=self, accepted=True).first()
        options =  list(Option.objects.filter(question=self, accepted=False)[0:4])
        shuffle(options)
        options.append(correct_option)
        shuffle(options)
        return options

    def chk_answer(self, text):
        os = Option.objects.filter(question=self, text=text)
        if len(os)==1:
            accepted = os.first().accepted
        elif len(os)==0:
            accepted = False
        else:
            raise MultipleObjectsReturned("Multiple options for %s" % repr(self))
        return accepted

    options = property(get_options)


class Option(models.Model):
    serial = models.CharField(max_length=12, unique=True)
    question = models.ForeignKey('Question', related_name="option_question")
    text = models.TextField()
    accepted = models.BooleanField(default=True)

    def __str__(self):
        return "(%s) %s%s" % (repr(self.question), self.text, ' rejected' if not self.accepted else '')

    def __repr__(self):
        return "O%s" % self.serial
