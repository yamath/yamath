from django.contrib import admin

from .models import Classroom, ClassroomUser, Topic, Score, TopicClassroom, TopicDependency, Option, QuestionMultiple, QuestionBoolean, QuestionOpen

admin.site.register(Classroom)
admin.site.register(ClassroomUser)
admin.site.register(Topic)
admin.site.register(Score)
admin.site.register(TopicClassroom)
admin.site.register(TopicDependency)
admin.site.register(Option)
admin.site.register(QuestionMultiple)
admin.site.register(QuestionBoolean)
admin.site.register(QuestionOpen)
