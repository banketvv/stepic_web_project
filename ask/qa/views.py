from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, render
from django.core.paginator import Paginator, EmptyPage
from .forms import *
from datetime import datetime, timedelta


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def latest_questions(request):
    latest_questions_list = Question.objects.all()
    latest_questions_list = latest_questions_list.order_by('-id')
    paginator = paginate(request, latest_questions_list)

    return render_to_response('list.html',
                              {
                                  "question_list": paginator,
                              })


def popular_questions(request):
    popular_questions_list = Question.objects.all()
    popular_questions_list = popular_questions_list.order_by('-rating')
    paginator = paginate(request, popular_questions_list)

    return render_to_response('list.html',
                              {
                                  "question_list": paginator,
                              })


def question(request, num):
    try:
        question_object = Question.objects.get(id=int(num))
    except ValueError:
        raise Http404
    except Question.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            answer = form.save()
            url = question_object.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question_object.id})

    return render(request,
                  'question.html',
                  {
                      "question": question_object,
                      "form": form,
                      "user": request.user,
                  })


def question_add(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        print (request.user)
        form._user = request.user
        if form.is_valid():
            ask = form.save()
            url = ask.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()

    return render(request,
                  'new_question.html',
                  {
                      "form": form,
                      "user": request.user,
                  })


def log_in(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            url = request.POST.get('continue', '/')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                sessid = do_login(request, username)
                if sessid:
                    response = HttpResponseRedirect(url)
                    response.set_cookie('sessid', sessid, expires=datetime.now() + timedelta(days=5))
                    return response
                else:
                    error = u'Wrong login and/or password'
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()

    return render(request,
                  'login.html',
                  {
                      "form": form,
                  })


def do_login(request, _login):
    try:
        user = User.objects.get(username=_login)
    except User.DoesNotExist:
        return None
    session = Session()
    session.key = request.session.session_key
    session.user = user
    session.expires = datetime.now() + timedelta(days=5)
    session.save()
    return session.key


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            url = request.POST.get('continue', '/')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return HttpResponseRedirect(url)
    else:
        form = SignupForm()

    return render(request,
                  'signup.html',
                  {
                      "form": form,
                  })
