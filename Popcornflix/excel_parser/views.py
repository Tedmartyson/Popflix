from django.views.generic import TemplateView
from .forms import UploadExcelForm
from .excel_parser import excel_parse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from catalog.models import House


@method_decorator(login_required(login_url='login'), name='dispatch')
class ParserView(TemplateView):
    template_name = 'excel_parser/parser.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request):
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_houses = excel_parse(request.FILES['file'])

            for house in excel_houses:
                h = House(**house)
                h.save()
            
        return render(request, self.template_name)