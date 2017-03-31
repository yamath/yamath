from blooming.models import *
from random import choice
import logging

for bloomer in Bloomer.objects.all():
    scores = [ score for score in Score.objects.filter(user=bloomer.user) if score.value > 0 ]
    for i in range(10):
        try:
            score = choice(scores)
            print("forget %s - %s" % (bloomer.user.username, score.topic))
            bloomer.add_scorevalue_of(score.topic, -1)
        except:
            pass

logging.info("Everybody forgot something")