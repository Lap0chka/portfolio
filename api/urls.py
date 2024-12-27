from django.urls import path

from api.views import BlogDetailView, BlogListView, PortfolioListView

urlpatterns = [
    path("portfolios/", PortfolioListView.as_view(), name="portfolio-list"),
    path("posts/", BlogListView.as_view(), name="blog-list"),
    path("post/<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
]
