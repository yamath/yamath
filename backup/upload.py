# import blooming.models as blooming
# from django.contrib.auth.models import User
# from blooming.models import *
# import backup.datadump as dump

# for (username, password) in dump.users:
#    u = User(username=username)
#    u.save()
#    u.password = password
#    u.save()
#    b = Bloomer(user=u)
#    b.save()
# me = User.objects.get(username='admin')
# me.is_staff = True
# me.is_admin = True
# me.is_superuser = True
# me.save()

# clink = {}
# for (pk, serial) in dump.classrooms:
#     c = Classroom(serial=serial)
#     c.save()
#     clink[pk] = c.pk

# for (username, cpk) in dump.classroombloomers:
#     cb = ClassroomBloomer(
#         bloomer=Bloomer.objects.get(user=User.objects.get(username=username)),
#         classroom=Classroom.objects.get(pk=clink[cpk])
#     )
#     cb.save()

# print("User: done")

# tlink = {}

# for (tpk, text) in dump.topics:
#     t = Topic(text=text)
#     t.save()
#     tlink[tpk] = t.pk

# for (a, p) in dump.topictopics:
#     td = TopicDependency(
#         ante=Topic.objects.get(pk=tlink[a]),
#         post=Topic.objects.get(pk=tlink[p]))
#     td.save()

# for (t, c) in dump.topicclassroom:
#     tc = TopicClassroom(
#         topic=Topic.objects.get(pk=tlink[t]),
#         classroom=Classroom.objects.get(pk=clink[c]),
#     )
#     tc.save()

# print("Topics: done")

# qlink = {}
# for (qpk, text, tpk, something, kind) in dump.questions:
#     q = Question(text=text, topic=Topic.objects.get(pk=tlink[tpk]), kind=kind)
#     q.save()
#     qlink[qpk] = q.pk

# print("Question:done")

# for (username, qpk, text, status, submit, interval) in dump.options:
#     if qpk==None:
#         continue
#     question = Question.objects.get(pk=qlink[qpk])
#     others = Option.objects.filter(question=question, text=text)
#     if len(others)==0:
#         o = Option(
#             question = question,
#             text = text,
#             status=status)
#         o.save()

# print("Option: done")

# for (username, tpk, value) in dump.scores:
#     s = Score(
#         user=User.objects.get(username=username),
#         topic=Topic.objects.get(pk=tlink[t]),
#         value=value)
#     s.save()