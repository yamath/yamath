from django.contrib import admin

from .models import *

admin.site.register(Bloomer)
admin.site.register(Classroom)
admin.site.register(ClassroomBloomer)
admin.site.register(Topic)
admin.site.register(TopicDependency)
admin.site.register(TopicClassroom)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Score)
# admin.site.register(Collection)
