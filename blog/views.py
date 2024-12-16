from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from blog.models import Blog
from .form import FormSuggest


class MyBlogListView(ListView):
    template_name = 'blog/posts.html'
    paginate_by = 6
    model = Blog
    context_object_name = "posts"
    success_url = reverse_lazy('blog')
    form_class = FormSuggest

    def get_queryset(self):
        language = self.request.LANGUAGE_CODE
        posts = Blog.objects.all()
        return posts



class DetailPageView(DetailView):
    model = Blog
    template_name = 'blog/detail.html'

    def get_success_url(self):
        return reverse_lazy('detail', args=(self.object.id,))



