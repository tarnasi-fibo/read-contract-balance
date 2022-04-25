from django.urls import path

from .views import total_supply, main_page

urlpatterns = [
    path('', main_page),
    path('total', total_supply),
]
