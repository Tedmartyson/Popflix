from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from catalog.models import House, Auction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic.detail import DetailView
from .forms import UploadRateForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from .filters import HouseFilter


@method_decorator(login_required(login_url='login'), name='dispatch')
class CatalogListView(ListView):
    
    model = House
    template_name = 'catalog/catalog.html'
    paginate_by = 9

    ordering = ['address']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_proposals'] = [x.id for x in self.request.user.liked_users_house_set.all()]
        context['filter'] = HouseFilter(self.request.GET, queryset=self.get_queryset())
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class CatalogDetailView(DetailView):
    
    model = House
    template_name = 'catalog/offer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auction'] = [
            {'rate': x.rate, 'user': User.objects.get(id=x.user_id), 'auction_id': x.id}
            for x in kwargs['object'].auction_house_set.all()
        ]
        return context


class LoginView(TemplateView):
    template_name = 'catalog/login.html'

    def get(self, request):
        context = {
            'form': AuthenticationForm(),
            'redirect_url': self.request.GET.get('next')
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is None:
                return render(request, self.template_name)

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(request, self.template_name)

            login(request, user)

            return redirect(self.request.POST.get('redirect_url', '/'))
            
        return render(request, self.template_name)

class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('login')


def add_to_favorite(request, pk, current_page):
    house = House.objects.get(id=pk)

    if house in request.user.liked_users_house_set.all():
        pass
    else:
        request.user.liked_users_house_set.add(house)
    return redirect(f'/?page={current_page}')


def auction_rate(request, pk):
    form = UploadRateForm(request.POST)
    if form.is_valid():
        rate = form.cleaned_data.get('rate')
        
        house = House.objects.get(id=pk)
        Auction.objects.create(user=request.user, house=house, rate=rate)

    return redirect(f'/catalog/{pk}')


def delete_auction(request, pk, pk2):
    a = Auction.objects.get(id=pk2)

    if a.user.id != request.user.id:
        return HttpResponse('<h1>Вы не можете удалить ставку другого пользователя</h1>')
    else:
        a.delete()
    return redirect(f'/catalog/{pk}')
