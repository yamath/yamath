import blooming.models as blooming
import content.models as content

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
    t = content.Topic(serial=s.serial+'000', name="Transational topic", serie=s)
    t.save()

# for tc in blooming.TopicClassroom.objects.all():
#     tc = TopicClassroom(
#         topic=Topic.objects.filter(serie=Serie.objects.get(pk=tlink[t])).first(),
#         classroom=Classroom.objects.get(pk=clink[c]),
#     )
#     tc.save()

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

print("Option:done")

# for (username, tpk, value) in dump.scores:
#     Score(
#         user=User.objects.get(username=username),
#         topic=Topic.objects.get(serie=Serie.objects.get(pk=tlink[t])).first(),
#         value=value).save()