from django.shortcuts import render
from django.views.generic import ListView
from portfolio.models import Portfolio


class BaseTemplateView(ListView):
    model = Portfolio
    template_name = 'portfolio/base.html'



