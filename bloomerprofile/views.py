import bloomerprofile.models as bloomingprofile
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import never_cache
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text
from content.models import *
from .models import *
import bloomerprofile.htmlhelpers as html

def requestPostSafeGet(request, key, default=None):
    try:
        return request.POST[key]
    except Exception as e:
        print("requestPostGetOrNone({}, {}) \n {}".format(request, key, e))
        return default
    
def sendEnvelope(request):
    sender = Bloomer.objects.get(username=request.POST['senderUsername'])
    receiver = Bloomer.objects.get(username=request.POST['receiverUsername'])
    text = requestPostSafeGet(request, 'text', '')
    # serie topic question option
    Envelope.objects.create(sender=sender, receiver=receiver, text=text)
    return HttpResponse("false")

def loadDoneSeries(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    return HttpResponse(html.loadDoneSeries(bloomer))

def loadTodoSeries(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    return HttpResponse(html.loadTodoSeries(bloomer))

def loadLateSeries(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    return HttpResponse(html.loadLateSeries(bloomer))

def loadQuestionText(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    question = Question.objects.get(serial=request.POST['questionSerial'])
    return HttpResponse(html.loadQuestionText(bloomer, question))

def loadQuestionForm(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    question = Question.objects.get(serial=request.POST['questionSerial'])
    return HttpResponse(html.loadQuestionForm(bloomer, question))

def chooseQuestion(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    serie = Serie.objects.get(serial=request.POST['serieSerial'])
    serial = choice(sorted(serie.topics, key=lambda t: bloomer.get_mean_of_topic(t))[0].questions).serial
    return HttpResponse(serial)

def submitAnswer(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    question = Question.objects.get(serial=request.POST['questionSerial'])
    answer = request.POST['answer']
    if bloomer.chk_answer(question, answer):
        return HttpResponse('true')
    else:
        return HttpResponse('false')

def unansweredQuestion(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    question = Question.objects.get(serial=request.POST['questionSerial'])
    bloomer.add_unanswered(question.topic)
    return HttpResponse('true')