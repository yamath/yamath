from django.contrib import admin

from .models import Topic, TopicDependency, Question, Answer, Score

admin.site.register(Topic)
admin.site.register(TopicDependency)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Score)
