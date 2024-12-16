from django.urls import path
from blog import views

urlpatterns = [
    path("", views.MyBlogListView.as_view(), name='blog'),
    path("page/<int:page>/", views.MyBlogListView.as_view(), name='paginator'),
    path("<slug:slug>", views.DetailPageView.as_view(), name='detail'),
]

