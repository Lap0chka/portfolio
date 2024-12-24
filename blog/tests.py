import uuid
from unittest.mock import MagicMock, patch

from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponse
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from blog.forms import CommentForm, SuggestionForm
from blog.models import Blog, Comment
from blog.views import MyBlogListView


class DetailPageViewTests(TestCase):
    """Tests for the DetailPageView."""

    def setUp(self) -> None:
        """Set up the test data for each test case."""
        self.my_post = Blog.objects.create(
            title="Test Blog Post",
            slug="test-blog-post",
            description="Test Blog Post Description",
            article="The post about test blog",
        )

        self.client = Client()
        self.url = reverse("detail", kwargs={"slug": self.my_post.slug})

    def test_get_increments_view_count(self) -> None:
        """Test that accessing the detail page increments the view count."""
        self.assertEqual(self.my_post.views, 0)  # Initial view count should be 0
        self.client.get(self.url)
        self.my_post.refresh_from_db()
        self.assertEqual(self.my_post.views, 1)

    def test_context_includes_comments_and_form(self) -> None:
        """Test that the context contains comments and the comment form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("comments", response.context)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], CommentForm)

    @patch("blog.views.send_custom_email")
    def test_post_valid_comment(self, mock_send_email: MagicMock) -> None:
        """Test that a valid comment is posted and email notification is sent."""
        data = {
            "username": "Test User",
            "body": "This is a test comment.",
        }

        # Set up session with a unique user ID
        session = self.client.session
        session["user_id"] = str(uuid.uuid4())
        session.save()

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after posting

        # Check that the comment was created
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertIsNotNone(comment)
        if comment:
            self.assertEqual(comment.username, data["username"])
            self.assertEqual(comment.body, data["body"])
            self.assertEqual(comment.post, self.my_post)

        # Check that the email was sent
        mock_send_email.assert_called_once_with(
            "NEW COMMENT",
            f"Check it\nThe username is {data['username']}\nThe body is {data['body']}",
        )

    def test_post_rate_limit(self) -> None:
        """Test that a user cannot post more than one comment within 60 minutes."""
        user_id = str(uuid.uuid4())
        session = self.client.session
        session["user_id"] = user_id
        session.save()

        # Create an initial comment
        Comment.objects.create(
            user_id=user_id,
            post=self.my_post,
            body="First comment",
            created_at=timezone.now(),
        )

        data = {
            "username": "Test User",
            "body": "Second comment attempt.",
        }

        response = self.client.post(self.url, data, follow=True)
        self.assertContains(
            response, "You can only submit a comment once every 60 minutes."
        )

        # Ensure only one comment exists
        self.assertEqual(Comment.objects.count(), 1)

    def test_post_invalid_comment(self) -> None:
        """Test that invalid comment data does not create a comment."""
        data = {
            "username": "",  # Invalid because username is required
            "body": "",
        }

        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "This field is required."
        )  # Ensure form errors are shown

        # Ensure no comment is created
        self.assertEqual(Comment.objects.count(), 0)


class MyBlogListViewTests(TestCase):
    def setUp(self) -> None:
        """Set up test data and request factory."""
        self.factory = RequestFactory()
        self.blog1 = Blog.objects.create(
            title="Test Blog Post",
            slug="test-blog-post",
            description="Test Blog Post Description",
            article="The post about test blog",
            views=10,
        )
        self.blog2 = Blog.objects.create(
            title="Post 2",
            slug="post-2",
            description="Second Blog Post Description",
            article="The post about second blog",
            views=20,
        )

    def add_middleware(self, request: HttpRequest) -> None:
        """Add session and message middleware to the request."""
        session_middleware = SessionMiddleware(lambda r: HttpResponse())
        session_middleware.process_request(request)
        request.session.save()

        messages_middleware = MessageMiddleware(lambda r: HttpResponse())
        messages_middleware.process_request(request)
        setattr(request, "_messages", FallbackStorage(request))

    def test_get_queryset_sorted_by_views(self) -> None:
        """Test that the queryset is sorted by views when 'by_views' is in the URL."""
        request = self.factory.get(reverse("order_by_views"))
        view = MyBlogListView()
        view.request = request

        queryset = view.get_queryset()
        self.assertEqual(list(queryset), [self.blog2, self.blog1])

    def test_get_queryset_sorted_by_created_at(self) -> None:
        """Test that the queryset is sorted by creation date by default."""
        request = self.factory.get(reverse("blog"))
        view = MyBlogListView()
        view.request = request

        queryset = view.get_queryset()
        self.assertEqual(list(queryset), [self.blog2, self.blog1])

    def test_get_context_data_contains_form(self) -> None:
        """Test that the context contains the SuggestionForm."""
        response = self.client.get(reverse("blog"))

        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], SuggestionForm)

    @patch("blog.views.send_custom_email")
    def test_post_valid_form_sends_email_and_redirects(
        self, mock_send_email: MagicMock
    ) -> None:
        """Test that a valid form submission sends an email and redirects."""
        response = self.client.post(
            reverse("blog"),
            {
                "title": "Test Title",
                "description": "Test Description",
                "link": "https://example.com",
            },
        )

        # Check for successful redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("blog"))

        # Check that the email was sent
        mock_send_email.assert_called_once_with(
            "The user sent a suggestion",
            "Title: Test Title\nDescription: Test Description\nURL: https://example.com",
        )
