from django.urls import path
from blog import views

urlpatterns = [
    path("", views.MyBlogListView.as_view(), name='blog'),
    path("page/<int:page>/", views.MyBlogListView.as_view(), name='paginator'),
    path("filter/<str:old>", views.MyBlogListView.as_view(), name='categori'),
    path("<int:pk>", views.DeteilView.as_view(), name='detail'),
    path("test/", views.Test.as_view(), name=''),


]

