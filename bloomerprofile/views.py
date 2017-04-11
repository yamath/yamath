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

def classSafeGet(_class, key, default=None):
    try:
        return _class.objects.get(serial=key)
    except:
        try:
            return _class.objects.get(username=key)
        except:
            try:
                return _class.objects.get(name=key)
            except:
                try:
                    return _class.objects.get(pk=key)
                except:
                    return default
    
def classSafeGetFromRequestPost(request, _class, _key, default=None):
    key = requestPostSafeGet(request, _key, default)
    return classSafeGet(Serie, key, default) or classSafeGet(Topic, key, default) or classSafeGet(Question, key, default) or classSafeGet(Option, key, default) or classSafeGet(Envelope, key, default) or classSafeGet(Classroom, key, default) or classSafeGet(Bloomer, key, default)
    
def sendEnvelope(request):
    print("sendEnvelope", request.POST)
    sender = classSafeGetFromRequestPost(request, Bloomer, 'senderUsername')
    receiver = classSafeGetFromRequestPost(request, Bloomer, 'receiverUsername')
    serie = classSafeGetFromRequestPost(request, Serie, 'serieSerial')
    topic = classSafeGetFromRequestPost(request, Topic, 'topicSerial')
    question = classSafeGetFromRequestPost(request, Question, 'questionSerial')
    text = "({0}) {1}".format(requestPostSafeGet(request, 'answer', '__'), requestPostSafeGet(request, 'text', ''))
    # serie topic question option
    Envelope.objects.create(sender=sender, receiver=receiver, serie=serie, topic=topic, question=question, text=text)
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

def loadEnvelopes(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    return HttpResponse(html.loadEnvelopes(bloomer))

def loadQuestionText(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    question = Question.objects.get(serial=request.POST['questionSerial'])
    return HttpResponse(html.loadQuestionText(bloomer, question))

def loadQuestionForm(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    question = Question.objects.get(serial=request.POST['questionSerial'])
    return HttpResponse(html.loadQuestionForm(bloomer, question))

def deleteEnvelope(request):
    Envelope.objects.get(pk=request.POST['pk']).delete()
    return HttpResponse('done')

def chooseQuestion(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    serie = Serie.objects.get(serial=request.POST['serieSerial'])
    worstMean=min( bloomer.get_mean_of_topic(t) for t in serie.topics )
    serial = choice( [ q for m in Mean.objects.filter(bloomer=bloomer) if (m.mean <= worstMean and m.topic in serie.topics) for q in m.topic.questions ] ).serial
    return HttpResponse(serial)

def submitAnswer(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    question = Question.objects.get(serial=request.POST['questionSerial'])
    correct_answer = question.get_correct().text
    answer = request.POST['answer']
    if bloomer.chk_answer(question, answer):
        return HttpResponse('true')
    else:
        return HttpResponse(correct_answer)

def unansweredQuestion(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    question = Question.objects.get(serial=request.POST['questionSerial'])
    print("ununswered", bloomer, question)
    bloomer.add_unanswered(question.topic)
    return HttpResponse(question.topic.serial)