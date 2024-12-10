from django import forms
from blog.models import Suggest


class FormSuggest(forms.ModelForm):
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

