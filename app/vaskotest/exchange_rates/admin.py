from django.contrib import admin

from .models import ExchangeRate


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    search_fields = 'currency',
    list_filter = 'start_date', 'end_date'
