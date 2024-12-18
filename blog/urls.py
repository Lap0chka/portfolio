from django.urls import path
from blog import views

urlpatterns = [
    # Posts
    path("", views.MyBlogListView.as_view(), name='blog'),
    path("page/<int:page>/", views.MyBlogListView.as_view(), name='paginator'),
    path("by_views/", views.MyBlogListView.as_view(), name='order_by_views'),
    # Detail Post
    path("<slug:slug>", views.DetailPageView.as_view(), name='detail'),
]

