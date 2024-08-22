from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView

from .forms import PhoneForm, PinForm
from .models import Cake, Client
from .utils import get_code


# Create your views here.


class IndexView(TemplateView):
    template_name = 'cake/index.html'

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


# TODO: Регистрация
@require_POST
def registration(request):
    print(request.POST)
    if 'phone_number' in request.POST:
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            name = form.cleaned_data['name']
            code = get_code()
            client, created = Client.objects.get_or_create(phone_number=phone_number)
            if (not created) and (client.name != name):
                print('except')
                # except
                return JsonResponse({'status': 'error', 'errors': 'Имя не совпадает'})
            client.pin = code
            client.name = name
            client.save()

            request.session['verification_code'] = code
            request.session['phone_number'] = phone_number

            return JsonResponse({'status': 'success', 'phone_number': phone_number, 'code': code})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    elif 'pin' in request.POST:
        form = PinForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data['pin']
            saved_code = request.session.get('verification_code')
            phone_number = request.session.get('phone_number')
            if pin == saved_code:
                client = Client.objects.get(phone_number=phone_number)
                if (client is not None) and client.is_active:
                    login(request, client)
                    return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Неправильный пин-код'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})



