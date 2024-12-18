import uuid
from unittest.mock import patch

from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone

from blog.models import Blog, Comment
from blog.forms import CommentForm, SuggestionForm
from blog.views import MyBlogListView


class DetailPageViewTests(TestCase):
    """Tests for the DetailPageView."""

    def setUp(self):
        """Set up the test data for each test case."""
        self.my_post = Blog.objects.create(
            title="Test Blog Post",
            slug="test-blog-post",
            description="Test Blog Post Description",
            article="The post about test blog",
        )

        self.client = Client()
        self.url = reverse('detail', kwargs={'slug': self.my_post.slug})

    def test_get_increments_view_count(self):
        """Test that accessing the detail page increments the view count."""
        self.assertEqual(self.my_post.views, 0)  # Initial view count should be 0
        self.client.get(self.url)
        self.my_post.refresh_from_db()
        self.assertEqual(self.my_post.views, 1)

    def test_context_includes_comments_and_form(self):
        """Test that the context contains comments and the comment form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('comments', response.context)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], CommentForm)

    @patch('blog.views.send_custom_email')
    def test_post_valid_comment(self, mock_send_email):
        """Test that a valid comment is posted and email notification is sent."""
        data = {
            'username': 'Test User',
            'body': 'This is a test comment.',
        }

        # Set up session with a unique user ID
        session = self.client.session
        session['user_id'] = str(uuid.uuid4())
        session.save()

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after posting

        # Check that the comment was created
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.username, data['username'])
        self.assertEqual(comment.body, data['body'])
        self.assertEqual(comment.post, self.my_post)

        # Check that the email was sent
        mock_send_email.assert_called_once_with(
            'NEW COMMENT',
            f"Check it\nThe username is {data['username']}\nThe body is {data['body']}"
        )

    # def test_post_rate_limit(self):
    #     """Test that a user cannot post more than one comment within 60 minutes."""
    #     user_id = str(uuid.uuid4())
    #     session = self.client.session
    #     session['user_id'] = user_id
    #     session.save()
    #
    #     # Create an initial comment
    #     Comment.objects.create(
    #         user_id=user_id,
    #         post=self.blog,
    #         body='First comment',
    #         created_at=timezone.now()
    #     )
    #
    #     data = {
    #         'username': 'Test User',
    #         'body': 'Second comment attempt.',
    #     }
    #
    #     response = self.client.post(self.url, data, follow=True)
    #     self.assertContains(response, 'You can only submit a comment once every 60 minutes.')
    #
    #     # Ensure only one comment exists
    #     self.assertEqual(Comment.objects.count(), 1)
    #
    # def test_post_invalid_comment(self):
    #     """Test that invalid comment data does not create a comment."""
    #     data = {
    #         'username': '',  # Invalid because username is required
    #         'body': '',
    #     }
    #
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'This field is required.')  # Ensure form errors are shown
    #
    #     # Ensure no comment is created
    #     self.assertEqual(Comment.objects.count(), 0)


# class MyBlogListViewTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.blog1 = Blog.objects.create(title="Test Blog Post",
#             slug="test-blog-post",
#             description="Test Blog Post Description",
#             article="The post about test blog", views=10)
#         self.blog2 = Blog.objects.create(title="Post 2", views=20)
#
#     def add_middleware(self, request):
#         """Добавляет необходимые middleware для тестирования сообщений и сессий."""
#         middleware = SessionMiddleware()
#         middleware.process_request(request)
#         request.session.save()
#
#         messages_middleware = MessageMiddleware()
#         messages_middleware.process_request(request)
#
#     def test_get_queryset_sorted_by_views(self):
#         request = self.factory.get(reverse('order_by_views'))
#         view = MyBlogListView()
#         view.request = request
#
#         queryset = view.get_queryset()
#         self.assertEqual(list(queryset), [self.blog2, self.blog1])
#
#     def test_get_queryset_sorted_by_created_at(self):
#         request = self.factory.get(reverse('blog'))
#         view = MyBlogListView()
#         view.request = request
#
#         queryset = view.get_queryset()
#         self.assertEqual(list(queryset), [self.blog1, self.blog2])
#
#     def test_get_context_data_contains_form(self):
#         request = self.factory.get(reverse('blog'))
#         view = MyBlogListView()
#         view.setup(request)
#         context = view.get_context_data()
#         self.assertIsInstance(context['form'], SuggestionForm)
#
#     @patch('blog.views.send_custom_email')
#     def test_post_valid_form_sends_email_and_redirects(self, mock_send_email):
#         request = self.factory.post(reverse('blog'), {
#             'title': 'Test Title',
#             'description': 'Test Description',
#             'url': 'http://example.com'
#         })
#         self.add_middleware(request)
#
#         view = MyBlogListView()
#         view.setup(request)
#
#         response = view.post(request)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, reverse('blog'))
#         mock_send_email.assert_called_once_with(
#             'The user sent a suggestion',
#             'Title: Test Title\nDescription: Test Description\nURL: http://example.com'
#         )
#
#     @patch('blog.views.send_custom_email', side_effect=Exception('Email Error'))
#     def test_post_email_error_logs_and_redirects(self, mock_send_email):
#         request = self.factory.post(reverse('blog'), {
#             'title': 'Test Title',
#             'description': 'Test Description',
#             'url': 'http://example.com'
#         })
#         self.add_middleware(request)
#
#         view = MyBlogListView()
#         view.setup(request)
#
#         response = view.post(request)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, reverse('blog'))
#         mock_send_email.assert_called_once()
#
#     def test_post_invalid_form_renders_with_errors(self):
#         """Тест отображения формы с ошибками при недопустимых данных."""
#         request = self.factory.post(reverse('blog'), {
#             'title': '',  # Некорректные данные: пустой заголовок
#             'description': '',
#             'url': ''
#         })
#         self.add_middleware(request)
#
#         view = MyBlogListView()
#         view.setup(request)
#
#         response = view.post(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'This field is required')