from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView


from .forms import PhoneForm, PinForm, ClientEditForm
from .models import Cake, CakeLevel, CakeShape, CakeTopping, CakeBerry, CakeDecor, Client
from .utils import get_code


class IndexView(TemplateView):
    template_name = 'cake/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['levels'] = CakeLevel.objects.all().order_by('price')
        context['shapes'] = CakeShape.objects.all().order_by('price')
        context['toppings'] = CakeTopping.objects.all().order_by('price')
        context['berries'] = CakeBerry.objects.all().order_by('price')
        context['decors'] = CakeDecor.objects.all().order_by('price')
        context['cakes'] = Cake.objects.filter(is_published=True)
        return context


class CakeCatalogView(ListView):
    model = Cake
    template_name = 'cake/catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cakes'] = Cake.objects.filter(is_published=True)
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'cake/lk-order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        client = get_object_or_404(Client, phone_number=user.phone_number)

        context['title'] = 'Личный кабинет'
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        client = get_object_or_404(Client, phone_number=user.phone_number)
        form = ClientEditForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('lk')
        return self.get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'put':
            return self.put(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

@csrf_exempt
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
