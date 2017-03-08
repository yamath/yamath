from django.contrib.auth.models import User
from yapp.models import Topic, TopicDependency, Question, Answer, Score
users = [
    ('angulo',       'dacambiare'),
    ('cabrera',       'dacambiare'),
    ('cavenago',       'dacambiare'),
    ('chunga',       'dacambiare'),
    ('detomaso',       'dacambiare'),
    ('fontanot',       'dacambiare'),
    ('gereda',       'dacambiare'),
    ('goyzueta',       'dacambiare'),
    ('grados',       'dacambiare'),
    ('loechle',       'dacambiare'),
    ('marini',       'dacambiare'),
    ('ore',       'dacambiare'),
    ('passuello',       'dacambiare'),
    ('paz',       'dacambiare'),
    ('pinto',       'dacambiare'),
    ('rivera',       'dacambiare'),
    ('rovegno',       'dacambiare'),
    ('vega',       'dacambiare'),
    ('yon',       'dacambiare'),
    ('agustini',       'dacambiare'),
    ('alvarado',       'dacambiare'),
    ('ancherani',       'dacambiare'),
    ('castro',       'dacambiare'),
    ('chiappe',       'dacambiare'),
    ('chuquisengo',       'dacambiare'),
    ('delavega',       'dacambiare'),
    ('favaro',       'dacambiare'),
    ('gonzalesaltez',       'dacambiare'),
    ('guzman',       'dacambiare'),
    ('jordan',       'dacambiare'),
    ('leon',       'dacambiare'),
    ('malqui',       'dacambiare'),
    ('oddi',       'dacambiare'),
    ('parini',       'dacambiare'),
    ('salazar',       'dacambiare'),
    ('suriano',       'dacambiare'),
    ('tapia',       'dacambiare'),
    ('bellia',       'dacambiare'),
    ('bonnett',       'dacambiare'),
    ('cubasgutierrez',       'dacambiare'),
    ('cuneo',       'dacambiare'),
    ('fontana',       'dacambiare'),
    ('kosoy',       'dacambiare'),
    ('luna',       'dacambiare'),
    ('malpartida',       'dacambiare'),
    ('martinez',       'dacambiare'),
    ('moncloa',       'dacambiare'),
    ('otoya',       'dacambiare'),
    ('pagano',       'dacambiare'),
    ('paliza',       'dacambiare'),
    ('pun',       'dacambiare'),
    ('sanchez',       'dacambiare'),
    ('taramona',       'dacambiare'),
    ('trillo',       'dacambiare'),
    ('witch',       'dacambiare'),
    ('black',       'dacambiare'),
    ('campero',     'dacambiare'),
    ('carbajal',    'dacambiare'),
    ('cogorno',     'dacambiare'),
    ('cubas',       'dacambiare'),
    ('delgado',     'dacambiare'),
    ('diaz',        'dacambiare'),
    ('espinosa',    'dacambiare'),
    ('gonzales',    'dacambiare'),
    ('larrea',      'dacambiare'),
    ('lopez',       'dacambiare'),
    ('mariaza',     'dacambiare'),
    ('mendoza',     'dacambiare'),
    ('munive',      'dacambiare'),
    ('perez',       'dacambiare'),
    ('pescarmona',  'dacambiare'),
    ('surianomirko',     'dacambiare'),
    ('tello',       'dacambiare'),
    ('torri',       'dacambiare'),
    ('varela',      'dacambiare'),
    ('vargas',      'dacambiare'),
    ('vassallo',    'dacambiare'),
    ('velez',       'dacambiare'),
    ('zamora',      'dacambiare'),
    ]

def reset_users(l):
  User.objects.all().delete()
  Score.objects.all().delete()
  for (u, p) in l:
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