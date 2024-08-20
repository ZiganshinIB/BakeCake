from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import Cake


# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context

# TODO: Список тортов
class CakeListView(ListView):
    model = Cake
    template_name = 'cake/cake_list.html'
    context_object_name = 'cakes'

# TODO: Создание торта

# TODO: Личный кабинет



