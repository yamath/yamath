import blooming.models as blooming
import content.models as content
import bloomerprofile.models as bloomerprofile
from django.contrib.auth.models import User

tslink = {}
serial = '000'
onemore = lambda s: "{0:03}".format(int(s)+1)

for topic in blooming.Topic.objects.all():
    serial = onemore(serial)
    s = content.Serie(serial=serial, name=topic.text)
    s.save()
    tslink[topic.pk] = s

for td in blooming.TopicDependency.objects.all():
    ss = content.SerieSerie(
        ante=tslink[td.ante.pk],
        post=tslink[td.post.pk],)
    ss.save()

for s in content.Serie.objects.all():
    t = content.Topic(serial=s.serial+'000', name="Transitional topic", serie=s)
    t.save()

print("Topic: done")

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
for oldtopic in blooming.Topic.objects.all():
    serial = '000'
    for q in blooming.Question.objects.filter(topic=oldtopic):
        topic = content.Topic.objects.filter(serie=tslink[oldtopic.pk]).first()
        serial = onemore(serial)
        question = content.Question(   
            serial = topic.serial + serial,
            text=q.text,
            topic=topic,
            kind=klink[q.kind],)
        question.save()
        qlink[q.pk]=question

print("Question:done")

for oldq in blooming.Question.objects.all():
    serial = '000'
    for oldo in blooming.Option.objects.filter(question=oldq):
        question = qlink[oldq.pk]
        others = content.Option.objects.filter(question=question, text=oldo.text)
        if len(others)==0:
            serial = onemore(serial)
            o = content.Option(
                serial = question.serial + serial,
                question = question,
                text = oldo.text,
                accepted = True if oldo.status == 'a' else False,)
            o.save()

# print("Option:done")
# for oldb in blooming.Bloomer.objects.all():
#     b = bloomerprofile.Bloomer(username=oldb.username)
#     b.save()
#     b.password = oldb.user.password
#     b.save()
# print(bloomerprofile.Bloomer.objects.all())

for oldc in blooming.Classroom.objects.all():
    c = bloomerprofile.Classroom(name=oldc.serial)
    c.save()

for oldcb in blooming.ClassroomBloomer.objects.all():
    cb = bloomerprofile.ClassroomBloomer(
        bloomer=bloomerprofile.Bloomer.objects.get(username=oldcb.bloomer.user.username),
        classroom=bloomerprofile.Classroom.objects.get(name=oldcb.classroom.serial),)
    cb.save()

for oldtc in blooming.TopicClassroom.objects.all():
    sc = bloomerprofile.SerieClassroom(
        classroom=bloomerprofile.Classroom.objects.get(name=oldtc.classroom.serial),
        serie=tslink[oldtc.topic.pk],)
    sc.save()


auxm = bloomerprofile.Mean(bloomer=bloomerprofile.Bloomer.objects.all().first(), topic=bloomerprofile.Topic.objects.all().first())
vhdict = {}
for h in ['XXXXX', 'AXXXX', 'AAXXX', 'AAAXX', 'AAAAX', 'AAAAA']:
    auxm.history = h + 'XXXXX'
    vhdict[ int(100*auxm.mean) ] = str(auxm.history)
def value_to_history(value):
    return vhdict[min( v for v in vhdict.keys() if v >= value )]

for score in blooming.Score.objects.all():
    m = bloomerprofile.Mean(
        bloomer=bloomerprofile.Bloomer.objects.get(username=score.user.username),
        topic=bloomerprofile.Topic.objects.get(name="Transitional topic", serie=tslink[score.topic.pk]),
        history=value_to_history(score.value),)
    m.save()
    print(score.value, '→', m.mean)