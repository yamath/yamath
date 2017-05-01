from back import orm
import content.models as content
import bloomerprofile.models as profile

def derive():
    for bloomer in profile.Bloomer.objects.all():
        orm.new('User', 
            email='{}@nomail.com'.format(bloomer.username), 
            pplain='pass', 
            legacyUsername=bloomer.username,
            status='acti')
    for classroom in profile.Classroom.objects.all():
        orm.new('Classroom',
                name=classroom.name)
    for cb in profile.ClassroomBloomer.objects.all():
        orm.add('User',
                'classrooms',
                {'legacyUsername':cb.bloomer.username},
                'Classroom',
                {'name':cb.classroom.name})
    