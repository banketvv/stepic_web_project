from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage
from .models import Question, Answer


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
    latest_questions_list = latest_questions_list.order_by('-added_at')
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

    return render_to_response('question.html',
                              {
                                  "question": question_object,
                                  "answers_list": question_object.answer_set.all(),
                              })
