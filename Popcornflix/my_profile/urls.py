from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', MyProfileView.as_view(), name='my_profile'),
    path('parser/', include('excel_parser.urls')),
    path('delete_from_favorite/<int:pk>', delete_from_favorite, name='delete_from_favorite')
]
