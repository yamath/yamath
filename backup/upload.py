import blooming.models as blooming
from django.contrib.auth.models import User
from blooming.models import *
from backend.models import *
from content.models import *
import backup.datadump as dump

for (username, password) in dump.users:
   u = User(username=username)
   u.save()
   u.password = password
   u.save()
   b = Bloomer(user=u)
   b.save()
me = User.objects.get(username='admin')
me.is_staff = True
me.is_admin = True
me.is_superuser = True
me.save()

clink = {}
for (pk, serial) in dump.classrooms:
    c = Classroom(serial=serial)
    c.save()
    clink[pk] = c.pk

for (username, cpk) in dump.classroombloomers:
    cb = ClassroomBloomer(
        bloomer=Bloomer.objects.get(user=User.objects.get(username=username)),
        classroom=Classroom.objects.get(pk=clink[cpk])
    )
    cb.save()

print("User: done")

tlink = {}
serial = '000'
onemore = lambda s: "{0:03}".format(int(s)+1)

for (tpk, text) in dump.topics:
    serial = onemore(serial)
    s = Serie(serial=serial, name=text)
    s.save()
    tlink[tpk]=s.pk

for (a, p) in dump.topictopics:
    ss = SerieSerie(
        ante=Serie.objects.get(pk=tlink[a]),
        post=Serie.objects.get(pk=tlink[p])
    )
    ss.save()

for s in Serie.objects.all():
    t = Topic(serial=s.serial+'000', name="Transational topic", serie=s)
    t.save()

for (t, c) in dump.topicclassroom:
    tc = TopicClassroom(
        topic=Topic.objects.filter(serie=Serie.objects.get(pk=tlink[t])).first(),
        classroom=Classroom.objects.get(pk=clink[c]),
    )
    tc.save()

print("Topics: done")

qlink = {}
klink = {
    'ibool':'b',
    'pbool':'b',
    'imulti':'m',
    'pmulti':'m',
    'iopen':'o',
    'popen':'o',
    'delay':'t',
    'eval':'w',
}
for (qpk, text, tpk, something, kind) in dump.questions:
    topic = Topic.objects.filter(serie=Serie.objects.get(pk=tlink[t])).first()
    serial = '000'
    while True:
        serial = onemore(serial)
        try:
            q = Question(
                serial = topic.serial + serial,
                text=text,
                topic=topic,
                kind=klink[kind],)
            q.save()
        except:
            continue
        break
    qlink[qpk]=q.pk

print("Question:done")

for (username, qpk, text, status, submit, interval) in dump.options:
    if qpk==None:
        continue
    question = Question.objects.get(pk=qlink[qpk])
    others = Option.objects.filter(question=question, text=text)
    if len(others)==0:
        o = Option(
            serial = question.serial + onemore(max( o.serial for o in Option.objects.filter(question=question) )),
            question = question,
            text = text,
            accepted = True if status == 'a' else False,)
        o.save()

print("Option: done")

for (username, tpk, value) in dump.scores:
    Score(
        user=User.objects.get(username=username),
        topic=Topic.objects.get(serie=Serie.objects.get(pk=tlink[t])).first(),
        value=value).save()