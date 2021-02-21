from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ParserView.as_view(), name='excel_parser'),
]
