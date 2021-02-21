from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', CatalogListView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('catalog/<int:pk>/', CatalogDetailView.as_view(), name='offer'),
    path('add_to_favorite/<int:pk>/<int:current_page>', add_to_favorite, name='add_to_favorite'),
    path('auction_rate/<int:pk>', auction_rate, name='auction_rate'),
    path('delete_auction/<int:pk>/<int:pk2>', delete_auction, name='delete_auction')
]
