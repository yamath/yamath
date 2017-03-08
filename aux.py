from django.contrib.auth.models import User
from yapp.models import Classroom, ClassroomUser, Topic, Score, TopicClassroom, TopicDependency, Option, QuestionMultiple, QuestionBoolean, QuestionOpen
users = [
    ('ART2', 'angulo',       'dacambiare'),
    ('ART2', 'cabrera',       'dacambiare'),
    ('ART2', 'cavenago',       'dacambiare'),
    ('ART2', 'chunga',       'dacambiare'),
    ('ART2', 'detomaso',       'dacambiare'),
    ('ART2', 'fontanot',       'dacambiare'),
    ('ART2', 'gereda',       'dacambiare'),
    ('ART2', 'goyzueta',       'dacambiare'),
    ('ART2', 'grados',       'dacambiare'),
    ('ART2', 'loechle',       'dacambiare'),
    ('ART2', 'marini',       'dacambiare'),
    ('ART2', 'ore',       'dacambiare'),
    ('ART2', 'passuello',       'dacambiare'),
    ('ART2', 'paz',       'dacambiare'),
    ('ART2', 'pinto',       'dacambiare'),
    ('ART2', 'rivera',       'dacambiare'),
    ('ART2', 'rovegno',       'dacambiare'),
    ('ART2', 'vega',       'dacambiare'),
    ('ART2', 'yon',       'dacambiare'),
    ('SCI2', 'agustini',       'dacambiare'),
    ('SCI2', 'alvarado',       'dacambiare'),
    ('SCI2', 'ancherani',       'dacambiare'),
    ('SCI2', 'castro',       'dacambiare'),
    ('SCI2', 'chiappe',       'dacambiare'),
    ('SCI2', 'chuquisengo',       'dacambiare'),
    ('SCI2', 'delavega',       'dacambiare'),
    ('SCI2', 'favaro',       'dacambiare'),
    ('SCI2', 'gonzalesaltez',       'dacambiare'),
    ('SCI2', 'guzman',       'dacambiare'),
    ('SCI2', 'jordan',       'dacambiare'),
    ('SCI2', 'leon',       'dacambiare'),
    ('SCI2', 'malqui',       'dacambiare'),
    ('SCI2', 'oddi',       'dacambiare'),
    ('SCI2', 'parini',       'dacambiare'),
    ('SCI2', 'salazar',       'dacambiare'),
    ('SCI2', 'suriano',       'dacambiare'),
    ('SCI2', 'tapia',       'dacambiare'),
    ('ART1', 'bellia',       'dacambiare'),
    ('ART1', 'bonnett',       'dacambiare'),
    ('ART1', 'cubasgutierrez',       'dacambiare'),
    ('ART1', 'cuneo',       'dacambiare'),
    ('ART1', 'fontana',       'dacambiare'),
    ('ART1', 'kosoy',       'dacambiare'),
    ('ART1', 'luna',       'dacambiare'),
    ('ART1', 'malpartida',       'dacambiare'),
    ('ART1', 'martinez',       'dacambiare'),
    ('ART1', 'moncloa',       'dacambiare'),
    ('ART1', 'otoya',       'dacambiare'),
    ('ART1', 'pagano',       'dacambiare'),
    ('ART1', 'paliza',       'dacambiare'),
    ('ART1', 'pun',       'dacambiare'),
    ('ART1', 'sanchez',       'dacambiare'),
    ('ART1', 'taramona',       'dacambiare'),
    ('ART1', 'trillo',       'dacambiare'),
    ('ART1', 'witch',       'dacambiare'),
    ('MED3', 'black',       'dacambiare'),
    ('MED3', 'campero',     'dacambiare'),
    ('MED3', 'carbajal',    'dacambiare'),
    ('MED3', 'cogorno',     'dacambiare'),
    ('MED3', 'cubas',       'dacambiare'),
    ('MED3', 'delgado',     'dacambiare'),
    ('MED3', 'diaz',        'dacambiare'),
    ('MED3', 'espinosa',    'dacambiare'),
    ('MED3', 'gonzales',    'dacambiare'),
    ('MED3', 'larrea',      'dacambiare'),
    ('MED3', 'lopez',       'dacambiare'),
    ('MED3', 'mariaza',     'dacambiare'),
    ('MED3', 'mendoza',     'dacambiare'),
    ('MED3', 'munive',      'dacambiare'),
    ('MED3', 'perez',       'dacambiare'),
    ('MED3', 'pescarmona',  'dacambiare'),
    ('MED3', 'surianomirko',     'dacambiare'),
    ('MED3', 'tello',       'dacambiare'),
    ('MED3', 'torri',       'dacambiare'),
    ('MED3', 'varela',      'dacambiare'),
    ('MED3', 'vargas',      'dacambiare'),
    ('MED3', 'vassallo',    'dacambiare'),
    ('MED3', 'velez',       'dacambiare'),
    ('MED3', 'zamora',      'dacambiare'),
    ]

def reset_users(l):
  User.objects.all().delete()
  Score.objects.all().delete()
  for (c, u, p) in l:
    User.objects.create_user(u, 'nomail@example.com', p)

def dump_database():
    f = open('dump.py', 'w')
    #TOPIC
    s = "topic_info = ["
    for t in Topic.objects.all():
        s += repr((t.serial, t.description)) + ', '
    s += ']\n'
    f.write(s)
    #TOPIC_DEPENDENCY
    s = "topicdependency_info = ["
    for t in TopicDependency.objects.all():
        s += repr((t.ante.serial, t.post.serial)) + ', '
    s += ']\n'
    f.write(s)
    #SCORE
    s = "score_info = ["
    for t in Score.objects.all():
        s += repr((t.user.username, t.topic.serial, t.value)) + ', '
    s += ']\n'
    f.write(s)
    #QUESTION
    s = "question_info = ["
    for t in Question.objects.all():
        s += repr((int(t.pk), t.text, t.topic.serial, t.notes)) + ', '
    s += ']\n'
    f.write(s)
    #ANSWERS
    s = "answer_info = ["
    for t in Answer.objects.all():
        s += repr((t.question.pk, t.answer, t.status)) + ', '
    s += ']\n'
    f.write(s)
    f.close()

def extoma():
    for serial in ['ART2', 'SCI2', 'ART1', 'MED3']:
        Classroom(serial=serial).save()
    for (c, u, p) in users:
        ClassroomUser(user=User.objects.get(username=u), classroom=Classroom.objects.get(serial=c)).save()
