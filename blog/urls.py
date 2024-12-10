from django.urls import path
from blog import views

urlpatterns = [
    path("", views.MyBlogListView.as_view(), name='blog'),
    path("page/<int:page>/", views.MyBlogListView.as_view(), name='paginator'),
    path("ordering/<str:ordering>", views.MyBlogListView.as_view(), name='ordering'),
    path("<int:pk>", views.DeteilView.as_view(), name='detail'),
]

