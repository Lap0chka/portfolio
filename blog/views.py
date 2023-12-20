from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, FormView
from blog.models import Blog
from django.urls import reverse_lazy,reverse
from blog.form import FormSuggest
from django.http import HttpResponseRedirect
from django.contrib import messages

class Test(TemplateView):
    template_name = 'blog/test.html'

class MyBlogListView(FormView, ListView):
    template_name = 'blog/base.html'
    paginate_by = 6
    model = Blog
    form_class = FormSuggest
    success_url = reverse_lazy('blog')

    def form_valid(self, form):
        try:
            form.save()
            # успешное сообщение
            messages.success(self.request, f'Thanks for the suggestions\nI will check and add)')
        except Exception:
            # ошибка
            messages.error(self.request, 'Something is wrong. Try again')
        return HttpResponseRedirect(self.get_success_url())

    def get_queryset(self):
        filt = self.kwargs.get('old')
        return Blog.objects.filter(is_published=True) if filt == 'old' else Blog.objects.order_by('-data')
   



class DeteilView(DetailView):
    model = Blog
    template_name = 'blog/detail.html'

    def get_success_url(self):
        return reverse_lazy('detail', args=(self.object.id,))



