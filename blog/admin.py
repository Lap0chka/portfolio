from django.contrib import admin
from parler.admin import TranslatableAdmin
from blog.models import Blog, Suggest


@admin.register(Blog)
class BlogAdmin(TranslatableAdmin):
    list_display = ('title', 'slug','created_at')

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}

@admin.register(Suggest)
class SuggestAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')