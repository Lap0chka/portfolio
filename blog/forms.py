from django import forms
from django.core.exceptions import ValidationError
from blog.models import Suggest, Comment
from blog.utills import check_swearing


class SuggestionForm(forms.ModelForm):
    """
    A form for submitting suggestions with a title, description, and an optional link.
    """

    title = forms.CharField(
        max_length=128,
        min_length=2,
        widget=forms.TextInput(attrs={
            'class': 'u-fullwidth',
            'placeholder': 'Enter Title',
        })
    )

    description = forms.CharField(
        max_length=256,
        widget=forms.TextInput(attrs={
            'class': 'u-fullwidth',
            'placeholder': 'Enter Description',
        })
    )

    link = forms.URLField(
        max_length=256,
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'u-fullwidth',
            'placeholder': 'Enter URL',
        })
    )

    class Meta:
        model = Suggest
        fields = '__all__'


class CommentForm(forms.ModelForm):
    """
    A form for submitting comments on blog posts.

    Fields:
        username (str): The name of the user submitting the comment.
        body (str): The content of the comment.
    """

    username = forms.CharField(
        max_length=128,
        min_length=2,
        widget=forms.TextInput(attrs={
            'class': 'u-fullwidth',
            'placeholder': 'John Smith',
        })
    )

    body = forms.CharField(
        max_length=1024,
        widget=forms.Textarea(attrs={
            'class': 'u-fullwidth',
            'placeholder': 'I think it is a great post!',
            'rows': 6,
        })
    )

    class Meta:
        model = Comment
        fields = ('username', 'body')

    def clean_username(self) -> str:
        """
        Validate the username to ensure it does not contain any profanity.

        Returns:
            str: The cleaned username.

        Raises:
            ValidationError: If profanity is detected in the username.
        """
        username = self.cleaned_data.get('username', '').strip()
        if check_swearing(username):
            raise ValidationError("You cannot use swearing words in the username.")
        return username

    def clean_body(self) -> str:
        """
        Validate the body to ensure it does not contain any profanity.

        Returns:
            str: The cleaned body of the comment.

        Raises:
            ValidationError: If profanity is detected in the body.
        """
        body = self.cleaned_data.get('body', '').strip()
        if check_swearing(body):
            raise ValidationError("You cannot use swearing words in the body.")
        return body

