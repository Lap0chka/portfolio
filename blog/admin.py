from django.contrib import admin
from blog.models import Blog, Suggest


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'data')

@admin.register(Suggest)
class SuggestAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')