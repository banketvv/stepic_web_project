from django import forms
from models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class AskForm(forms.Form):
    title = forms.CharField(max_length=100, min_length=1)
    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        return self.cleaned_data

    def save(self):
        question = Question(**self.cleaned_data)
        question.author_id = self._user.id
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_question(self):
        question_id = self.cleaned_data['question']
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            question = None
        return question

    def clean(self):
        return self.cleaned_data

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author_id = self._user.id
        answer.save()
        return answer


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Empty username field!')
        try:
            User.objects.get(username=username)
            raise forms.ValidationError('Exists user with the same name!')
        except User.DoesNotExist:
            pass
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.strip() == '':
            raise forms.ValidationError('Empty email field!')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 3:
            raise forms.ValidationError('Password is too short!')
        return password

    def clean(self):
        return self.cleaned_data

    def save(self):
        user = User.objects.create_user(self.clean_username(), self.clean_email(), self.clean_password())
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Empty username field!')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Wrong username and/or password!')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password is empty!')
        return password

    def clean(self):
        return self.cleaned_data

