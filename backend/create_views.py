from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache
import blooming.models as blooming
import backend.models as backend
from django.contrib import messages

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def create_bulk_bool(request):
    if request.method == 'GET':
        return render(request, 'backend/create_bulk_bool.html')
    elif request.method == 'POST':
        topic = blooming.Topic.objects.get(pk=request.POST['topic_pk'])
        kind = request.POST['kind']
        for (key, value) in [ (key[5:], value) for (key, value) in request.POST.items() if (key[:5]=='text_' and value!='')]:
            option_text = 'vero' if ('checkbox_%s' % key) in request.POST else 'falso'
            q = blooming.Question(topic=topic, text=value, kind=kind)
            q.save()
            o = blooming.Option(user=request.user, question=q, text=option_text, status='a')
            o.save()
        return redirect('backend:index')

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def create_multi(request):
    if request.method == 'GET':
        return render(request, 'backend/create_multi.html')
    elif request.method == 'POST':
        topic = blooming.Topic.objects.get(pk=request.POST['topic_pk'])
        q = blooming.Question(topic=topic, text=request.POST['text'], kind=request.POST['kind'])
        q.save()
        options = []
        for (key, value) in [ (key[11:], value) for (key, value) in request.POST.items() if (key[:11]=='optiontext_' and value!='')]:
            option_status = 'a' if ('checkbox_%s' % key) in request.POST else 'r'
            o = blooming.Option(user=request.user, question=q, text=value, status=option_status)
            o.save()
            options.append(o)
        return render(request, 'backend/create_multi.html', {'topic':topic, 'question':q, 'options':options})

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def create_topic(request):
    if request.method == 'GET':
        raise ValueError("Method GET not supported")
    elif request.method == 'POST':
        topic_text = request.POST['create_topic_text']
        try:
            topic = blooming.Topic.objects.get(text=topic_text)
            messages.error(request, "Topic already exists!")
        except blooming.models.ObjectDoesNotExist:
            topic = blooming.Topic(text=topic_text)
            topic.save()
        return redirect("backend:topic_details", pk=topic.pk)







