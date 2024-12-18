import uuid
from datetime import timedelta
from typing import Any, Dict

from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
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
    """
    A view to display a paginated list of blog posts and handle suggestion form submissions.

    Attributes:
        template_name (str): The template used for displaying the posts.
        paginate_by (int): Number of posts displayed per page.
        model (Blog): The model representing blog posts.
        context_object_name (str): The context variable name for the posts.
        success_url (str): The URL to redirect to after a successful form submission.
        form_class (SuggestionForm): The form class for handling suggestions.
    """

    template_name = 'blog/posts.html'
    paginate_by = 6
    model = Blog
    context_object_name = "posts"
    success_url = reverse_lazy('blog')
    form_class = SuggestionForm

    def get_queryset(self) -> Any:
        """
        Retrieve the queryset of blog posts, ordered by views or creation date.

        Returns:
            QuerySet: The ordered queryset of blog posts.
        """
        queryset = super().get_queryset()
        if 'by_views' in self.request.path:
            logger.info('Sorting posts by views.')
            return queryset.order_by('-views')
        logger.info('Sorting posts by creation date.')
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Add the suggestion form to the context.

        Args:
            **kwargs (Any): Additional context variables.

        Returns:
            Dict[str, Any]: The context dictionary with the suggestion form.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle the submission of the suggestion form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: A redirect response after handling the form.
        """
        logger.info('Processing suggestion form submission.')
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                link = form.cleaned_data.get('link', None)

                subject = 'The user sent a suggestion'
                message = f'Title: {title}\nDescription: {description}\nURL: {link or "No URL provided"}'

                send_custom_email(subject, message)
                logger.info(f'Suggestion email sent successfully: {title}, {link}')

                form.save()
                messages.success(request, 'Thank you for your suggestion!')
                return HttpResponseRedirect(self.success_url)

            except Exception as e:
                logger.error(f'Error sending suggestion email: {e}')
                messages.error(request, 'An error occurred while sending your suggestion email.')
                return redirect(self.success_url)

        logger.info('Suggestion form is invalid. Rendering form with errors.')
        return self.render_to_response(self.get_context_data(form=form))



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
