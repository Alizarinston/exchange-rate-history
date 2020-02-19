from django.urls import path

from .views import currency_list, delete_record, currency_history, CurrencyCreate

urlpatterns = [
    path('', currency_list, name='currency_list_url'),
    path('currency/<str:slug>/', currency_history, name='currency_history_url'),
    path('delete/<str:slug>/<str:start_date>/', delete_record, name='delete_record_url'),
    path('create/', CurrencyCreate.as_view(), name='currency_create_url')
]
