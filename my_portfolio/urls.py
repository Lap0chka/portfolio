from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from portfolio import views

urlpatterns = [
    path("admin/", admin.site.urls),
                  path('rosetta/', include('rosetta.urls')),

              ] + i18n_patterns(
    path("i18n/", include("django.conf.urls.i18n")),
    path("", views.BaseTemplateView.as_view(), name='portfolio'),
    path("blog/", include('blog.urls',)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)