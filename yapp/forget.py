from django.contrib.auth.models import User
from random import choice
from yapp.models import Classroom, ClassroomUser, Topic, Score, TopicClassroom

for user in User.objects.all():
  print('Forgetting', user.username)
  classroom = ClassroomUser.objects.get(user=user).classroom
  all_topics = [ tc.topic for tc in TopicClassroom.objects.filter(classroom=classroom) ]
  topics = []
  for t in all_topics:
    try:
      score = Score.objects.get(user=user, topic=t).value
    except Score.DoesNotExist:
      score = 0
    if score > 0:
      topics.append(t)
  for i in range(10):
    try:
      topic = choice(topics)
      score = Score.objects.get(user=user, topic=topic)
      score.value = max(0, score.value-1)
      score.save()
    except Exception as e:
      print("###forget error:", user.username, t, e)
