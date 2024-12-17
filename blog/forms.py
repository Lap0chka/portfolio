from datetime import datetime, timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from blog.models import Suggest, Comment
from blog.utills import check_swearing


class SuggestionForm(forms.ModelForm):
    title = forms.CharField(max_length=128, min_length=2, widget=forms.TextInput(attrs={
        'placeholder': "Enter Title",
    }))
    description = forms.CharField(max_length=256, widget=forms.TextInput(attrs={
        'placeholder': "Enter Description",
    }))
    link = forms.CharField(max_length=256, required=False, widget=forms.TextInput(attrs={
        'placeholder': "Enter url",
    }))
    class Meta:
        model = Suggest
        fields = '__all__'


class CommentForm(forms.ModelForm):
    username = forms.CharField(max_length=128, min_length=2, widget=forms.TextInput(attrs={
        'class': 'u-fullwidth',
        'placeholder': 'John Smith',
    }))
    body = forms.CharField(max_length=1024, widget=forms.Textarea(attrs={
        'class': 'u-fullwidth',
        'placeholder': 'I think it is a great post!',
        'rows': 6
    }))

    class Meta:
        model = Comment
        fields = ('username', 'body')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if check_swearing(username):
            raise ValidationError("You cannot use swearing words in the username.")
        return username

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if check_swearing(body):
            raise ValidationError("You cannot use swearing words in the body.")
        return body

