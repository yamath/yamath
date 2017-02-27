from django.contrib.auth.models import User
from .models import Question, Score, Topic, TopicDependency, Answer

# User
def repopulate_users():
  User.objects.all().delete()
  Score.objects.all().delete()
  users = [
    ('black',       'pass9019'),
    ('campero',     'pass9549'),
    ('carbajal',    'pass2351'),
    ('cogorno',     'pass1362'),
    ('cubas',       'pass2233'),
    ('delgado',     'pass3618'),
    ('diaz',        'pass1316'),
    ('espinosa',    'pass4467'),
    ('gonzales',    'pass6679'),
    ('larrea',      'pass8881'),
    ('lopez',       'pass6426'),
    ('mariaza',     'pass4400'),
    ('mendoza',     'pass3364'), 
    ('munive',      'pass7963'),
    ('perez',       'pass7582'),
    ('pescarmona',  'pass6324'),
    ('suriano',     'pass4831'),
    ('tello',       'pass6808'),
    ('torri',       'pass6135'),
    ('varela',      'pass6341'),
    ('vargas',      'pass6670'),
    ('vassallo',    'pass9570'),
    ('velez',       'pass9619'),
    ('zamora',      'pass2763'),
  ]
  for (u, p) in users:
    User.objects.create_user(u, 'nomail@example.com', p)

# Topic
def repopulate_topic():
  Topic.objects.all().delete()
  topics = [
    ('3000', 'Grandezze orientate e numeri relativi'),
    ('3001', 'La rappresentazine grafica dei numeri relativi'),
    ('3002', 'Somma algebrica dei numeri relativi'),
    ('3003', 'Moltiplicazione e divisione dei numeri relativi'),
    ('3004', 'Elevamento a potenza e radice di un numero relativo'),
    ('3005', 'I numeri relativi in fisica'),
    ('3006', 'I numeri relativi nelle attività socio-economiche'),
    ('3007', 'Le potenze di dieci nei fenomeni naturali'),
  ]
  for t in topics:
    Topic(serial=t[0], description=t[1]).save()

  TopicDependency.objects.all().delete()
  topics_dependencies = [
    ('3000', '3001'),
  ]
  for (ante, post) in topics_dependencies:
    TopicDependency(ante=Topic.objects.get(serial=ante), post=Topic.objects.get(serial=post)).save()

def repopulate_questions():
  Question.objects.all().delete()
  Answer.objects.all().delete()
  questions = [
    ('3000', "Scegli l'affermazione vera, indicando solo il numero corrispondente.<br />I numeri relativi:<ol><li>sono preceduti dal segno più</li><li>non sono preceduti da alcun segno</li><li>sono preceduti dal segno più o dal segno meno</li></ol>", '3'),
    ('3000', "Scegli l'affermazione vera, indicando solo il numero corrispondente.<br />L'insieme $\mathbb{Q}^+$ contiene:<ol><li>tutti gli elementi di $\mathbb{Z}$</li><li>tutti i numeri interi e razionali</li><li>tutti i numeri assoluti interi e razionali</li></ol>", '3'),
    ('3000', "Stabilisci se le seguente affermazione è vera o falsa. Scrivi esattamente 'vero' oppure 'falso'.<br />I numeri relativi servono per misurare grandezze orientate.", 'vero'),
    ('3000', "Stabilisci se le seguente affermazione è vera o falsa. Scrivi esattamente 'vero' oppure 'falso'.<br />$\mathbb{R}$ è un sottoinsieme di $\mathbb{R}^+$.", 'falso'),
  ]
  for (serial, content, answer) in questions:
    q = Question(text=content, topic=Topic.objects.get(serial=serial))
    q.save()
    Answer(question=q, answer=answer, status='ok').save()


