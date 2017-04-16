from django import forms
from models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=100, min_length=1)
    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        pass

    def save(self):
        question = Question(**self.cleaned_data)
        # To avoid NOT NULL author_id exception:
        question.author_id = 1
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean(self):
        pass

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer
