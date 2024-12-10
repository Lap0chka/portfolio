from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from blog.models import Blog
from django.urls import reverse_lazy
from .form import FormSuggest
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.db import models


class MyBlogListView(ListView):
    template_name = 'blog/base.html'
    paginate_by = 6
    model = Blog
    success_url = reverse_lazy('blog')
    form_class = FormSuggest

    def get_queryset(self):
        self.ordering = self.kwargs.get('ordering', '-data')
        if self.ordering not in ['data', '-data', 'views', '-views']:
            self.ordering = '-data'
        return Blog.objects.order_by(self.ordering)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Создайте экземпляр формы
        context['current_ordering'] = self.ordering
        print(context['current_ordering'])
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        link = request.POST.get('link')
        message_error = f'Something is wrong. Try again\n'
        print(form)
        if form.is_valid():
            try:
                form.save()
                subject = 'Новое предложение'
                message = f'Кто-то отправил мне предложение.\n' \
                          f'Тема: {form.cleaned_data["title"]}\n' \
                          f'Описание: {form.cleaned_data["description"]}\n' \
                          f'Ссылка: {form.cleaned_data["link"]}'
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = ['danya.tkachenko.1997@gmail.com']
                send_mail(subject, message, from_email, to_email, fail_silently=False)
                messages.success(self.request, f"Thanks for the suggestion\nI'll check and add")
            except Exception:
                messages.error(self.request, message_error)
            return super().get(request, *args, **kwargs)
        else:
            if not isinstance(link, models.URLField):
                message_error += f'\nURL field {link} is not url'
            messages.error(self.request, message_error)
            return redirect('blog')

class DeteilView(DetailView):
    model = Blog
    template_name = 'blog/detail.html'

    def get_success_url(self):
        return reverse_lazy('detail', args=(self.object.id,))

    def get_object(self, queryset=None):
        # Увеличиваем количество просмотров на 1 при каждом просмотре поста
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj



