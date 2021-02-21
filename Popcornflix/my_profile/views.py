from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from catalog.models import House


@method_decorator(login_required(login_url='login'), name='dispatch')
class MyProfileView(TemplateView):
    
    admin_template_name = 'my_profile/admin_profile.html'
    client_template_name = 'my_profile/client_profile.html'

    def get(self, request, **kwargs):
        template = self.admin_template_name if request.user.groups.all()[0].name == 'admin' else self.client_template_name
    
        context = {
            'favorite_houses': request.user.liked_users_house_set.all()
        }

        return render(request, template, context=context)

def delete_from_favorite(request, pk):
    request.user.liked_users_house_set.get(id=pk).delete()
    return redirect('my_profile')
