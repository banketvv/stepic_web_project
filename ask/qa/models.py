from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new():
        pass

    def popular(self):
        pass


class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, related_name="question_author")
    likes = models.ManyToManyField(User, related_name="question_likers")

    def __unicode__(self):
        return self.title

    def get_url(self):
        return "/question/{}/".format(self.id)


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.text


