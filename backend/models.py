from django.db import models
import blooming.models as blooming

class Claim(models.Model):
    bloomer = models.ForeignKey(blooming.Bloomer, related_name='claim_bloomer', blank=True, null=True)
    topic = models.ForeignKey(blooming.Topic, related_name='claim_topic', blank=True, null=True)
    question = models.ForeignKey(blooming.Question, related_name='claim_question', blank=True, null=True)
    option = models.ForeignKey(blooming.Option, related_name='claim_option', blank=True, null=True)
    text = models.TextField(blank=True, null=True)
