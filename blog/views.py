import uuid
from datetime import timedelta
from typing import Any, Dict

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView

from .forms import SuggestionForm, CommentForm
from .models import Blog, Comment
from .utills import send_custom_email
from logger.logger import Logger

# Initialize the logger
logger_instance = Logger(__name__)
logger = logger_instance.get_logger()


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
    """
    A detailed view for displaying a blog post and handling user comments.

    This view handles:
    - Displaying a single blog post based on the slug and language code.
    - Displaying associated comments and a form for submitting new comments.
    - Incrementing the view count each time the post is accessed.
    - Restricting users to submit one comment per 60 minutes.
    - Sending a notification email when a new comment is posted.
    """
    model = Blog
    template_name = 'blog/detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Add comments and the comment form to the context.

        Args:
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Dict[str, Any]: The context data with comments and the comment form.
        """
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object())
        context['form'] = self.form_class()
        logger.debug("Context data for post retrieved successfully")
        return context

    def get_object(self, *args: Any, **kwargs: Any) -> Blog:
        """
        Retrieve the blog post based on the current language and slug.

        Returns:
            Blog: The blog post object.
        """
        language = self.request.LANGUAGE_CODE
        post = get_object_or_404(
            Blog,
            translations__language_code=language,
            translations__slug=self.kwargs['slug']
        )
        return post

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Increment the post's view count on GET request.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
        post = self.get_object()
        post.views += 1
        post.save(update_fields=['views'])
        logger.info(f"Post '{post.title}' was viewed. Total views: {post.views}")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle the submission of a new comment.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: A redirect to the post's detail page or a response with form errors.
        """
        post = self.get_object()
        form = self.form_class(request.POST)

        if form.is_valid():
            # Ensure the user has a unique session identifier
            user_id: str = request.session.get('user_id', str(uuid.uuid4()))
            request.session['user_id'] = user_id

            # Check for the rate limit: one comment per 60 minutes
            last_comment = Comment.objects.filter(user_id=user_id, post=post).order_by('-created_at').first()
            if last_comment and timezone.now() - last_comment.created_at < timedelta(minutes=60):
                messages.error(request, 'You can only submit a comment once every 60 minutes. Please try again later.')
                logger.warning(f"User {user_id} attempted to post a comment too soon.")
                return redirect(post.get_absolute_url())

            # Save the new comment
            comment = form.save(commit=False)
            comment.user_id = user_id
            comment.post = post
            comment.save()

            # Send notification email
            username: str = form.cleaned_data['username']
            body: str = form.cleaned_data['body']
            message: str = f"Check it\nThe username is {username}\nThe body is {body}"
            send_custom_email('NEW COMMENT', message)

            logger.info(f"New comment posted by user '{username}' on post '{post.title}'")
            messages.success(request, 'Your comment has been posted.')
            return redirect(post.get_absolute_url())

        # Handle form errors
        for error in form.errors.values():
            messages.error(request, error)
            logger.error(f"Form submission error: {error}")

        return self.render_to_response(self.get_context_data(form=form))
