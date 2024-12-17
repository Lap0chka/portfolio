import uuid
from datetime import timedelta

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView

from blog.models import Blog, Comment
from .forms import SuggestionForm, CommentForm
from .utills import send_custom_email


class MyBlogListView(ListView):
    template_name = 'blog/posts.html'
    paginate_by = 6
    model = Blog
    context_object_name = "posts"
    success_url = reverse_lazy('blog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SuggestionForm()
        return context

class DetailPageView(DetailView):
    model = Blog
    template_name = 'blog/detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object())
        context['form'] = self.form_class()
        return context

    def get_object(self, *args, **kwargs):
        language = self.request.LANGUAGE_CODE
        post = get_object_or_404(
            Blog,
            translations__language_code=language,
            translations__slug=self.kwargs['slug']
        )
        return post

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = self.form_class(request.POST)

        if form.is_valid():
            if 'user_id' not in request.session:
                request.session['user_id'] = str(uuid.uuid4())
            user_id = request.session['user_id']
            last_comment = Comment.objects.filter(
                user_id=user_id, post=post
            ).order_by('-created_at').first()
            if last_comment and timezone.now() - last_comment.created_at < timedelta(minutes=60):
                messages.error(self.request, 'You can only submit a comment once every 60 minutes. '
                                             'Please try again later.')
                return redirect(post.get_absolute_url())

            comment = form.save(commit=False)
            comment.user_id = user_id
            comment.post = post
            comment.save()

            username = form.cleaned_data['username']
            body = form.cleaned_data['body']
            message = f"Check it\nThe username is {username}\nThe body is {body}"
            send_custom_email('NEW COMMENT', message)
            messages.success(self.request, 'Your comment has been posted')
            return redirect(post.get_absolute_url())

        for error in form.errors.values():
            messages.error(request, error)

        return self.render_to_response(self.get_context_data(form=form))
