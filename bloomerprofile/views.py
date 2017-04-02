# from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import never_cache
# from django.shortcuts import redirect, render
# from random import choice
# from content.models import *
# from blooming.models import *
import bloomerprofile.models as bloomingprofile
# import logging
from django.contrib import messages
# from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import never_cache
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text
from content.models import *
from .models import *
import bloomerprofile.htmlhelpers as html

# class LazyEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Serie):
#             return force_text(obj)
#         return super(LazyEncoder, self).default(obj)

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
# def selectSerie(request):
#     bloomer = Bloomer.objects.get(username=request.POST['username'])
#     serie = Serie.objects.get(name=request.POST['serieName'])
#     return HttpResponse(html.selectSerie(bloomer))

@never_cache
def ajax(request):
    bloomer = Bloomer.objects.get(username=request.POST['username'])
    if 'call' in request.POST:
        return HttpResponse(str(eval(request.POST['call'])))
    # datadict = {}
    # req_list = request.POST['request'].split()
    # for req in req_list:
    #     variable_name, call = req.split('=')
    #     print(variable_name, '=', call)
    #     datadict[variable_name] = eval(call)
    # print("Debug:", datadict)
    return JsonResponse(datadict)