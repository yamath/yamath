import blooming.models as blooming
from django.contrib.auth.models import User

f = open('backup/datadump.py', 'w')

users = [ (u.username, u.password) for u in User.objects.all() ]
f.write('users = '+repr(users)+'\n')

classrooms = [ (c.pk, c.serial) for c in blooming.Classroom.objects.all() ]
f.write('classrooms = '+repr(classrooms)+'\n')

f.write('classroombloomers = '+
        repr([ (cb.bloomer.user.username, cb.classroom.pk) for cb in blooming.ClassroomBloomer.objects.all() ])+
        '\n')

f.write('topics = '+
        repr([ (t.pk, t.text) for t in blooming.Topic.objects.all() ])+
        '\n')

f.write('topictopics = '+
        repr([ (tt.ante.pk, tt.post.pk) for tt in blooming.TopicDependency.objects.all() ])+
        '\n')

f.write('topicclassroom = '+
        repr([ (tc.topic.pk, tc.classroom.pk) for tc in blooming.TopicClassroom.objects.all() ])+
        '\n')

def getattr_or_none(obj, attr):
    try:
        return getattr(obj, attr)
    except AttributeError:
        return None

f.write('options = '+
        repr([ (getattr_or_none(o, 'user.username'), o.question.pk, o.text, o.status, repr(o.submit_time), o.interval) for o in blooming.Option.objects.all() ])+
        '\n')

f.write('questions = '+
        repr([ (q.pk, q.text, q.topic.pk, q.note, q.kind) for q in blooming.Question.objects.all() ])+
        '\n')

f.write('scores = '+
        repr([ (s.user.username, s.topic.pk, s.value) for s in blooming.Score.objects.all() ])+
        '\n')

f.close()

