from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exchange_rates/', include('exchange_rates.urls'))
]
