from django.contrib.auth.models import User
from random import choice
from tapp.models import Score, Topic

for user in User.objects.all():
  print('Forgetting', user.username)
  topics = []
  for t in Topic.objects.all():
    try:
      score = Score.objects.get(user=user.username, topic=t).value
    except Score.DoesNotExist:
      score = 0
    if score > 0:
      topics.append(t)
  for i in range(5):
    try:
      topic = choice(topics)
      score = Score.objects.get(user=user.username, topic=topic)
      score.value = max(0, score.value-1)
      score.save()
    except Exception as e:
      print("###forget error:", user.username, t, e)
