from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.core.paginator import Paginator, EmptyPage
from .models import Question, Answer
from .forms import AskForm, AnswerForm


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
                  })


def question_add(request):
    if request.method == "POST":
        form = AskForm(request.POST)
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
                  })
