from django.shortcuts import render, get_list_or_404, redirect
from django.views.generic import View
from .forms import ExchangeRateForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
import datetime

from .models import ExchangeRate


def currency_list(request):
    currencies = []
    distinct = ExchangeRate.objects.order_by().values('currency').distinct()
    for _ in distinct:
        currencies.append(ExchangeRate.objects.filter(currency=_['currency']).latest())

    return render(request, 'exchange_rates/currency_list.html', context={'currencies': currencies})


def currency_history(request, slug):
    records = get_list_or_404(ExchangeRate.objects.order_by('-start_date'), currency=slug)

    return render(request, 'exchange_rates/currency_history.html', context={'records': records, 'slug': slug})


def filter_records(initial, ratio):
    if ratio == 'gt':
        return ExchangeRate.objects.filter(start_date__gt=initial.start_date,
                                           currency=initial.currency)
    elif ratio == 'lt':
        return ExchangeRate.objects.filter(currency=initial.currency,
                                           start_date__lt=initial.start_date)
    else:
        raise Exception('There is no such ratio')


def delete_record(request, slug, start_date):
    if request.method == "POST":
        try:
            record = ExchangeRate.objects.get(currency=slug, start_date=start_date)
            if filter_records(record, 'lt').count():
                lt = filter_records(record, 'lt').latest()

                if filter_records(record, 'gt').count():
                    gt = filter_records(record, 'gt').earliest()
                    lt.end_date = datetime.datetime.strptime(str(gt.start_date),
                                                             '%Y-%m-%d') - datetime.timedelta(days=1)
                else:
                    lt.end_date = None
                lt.save(update_fields=['end_date'])

            record.delete()

            return HttpResponseRedirect("/exchange_rates/currency/{}".format(slug))

        except ExchangeRate.DoesNotExist:
            return HttpResponseNotFound("<h2>Record not found</h2>")

    return HttpResponseRedirect("/exchange_rates/currency/{}".format(slug))


class CurrencyCreate(View):
    def get(self, request):
        form = ExchangeRateForm()

        return render(request, 'exchange_rates/currency_create.html', context={'form': form})

    def post(self, request):
        bound_form = ExchangeRateForm(request.POST)

        if bound_form.is_valid():
            new_record = bound_form.save()

            if filter_records(new_record, 'lt').count():
                lt = filter_records(new_record, 'lt').latest()
                lt.end_date = datetime.datetime.strptime(str(new_record.start_date), '%Y-%m-%d') - datetime.timedelta(
                    days=1)
                lt.save(update_fields=['end_date'])

            if filter_records(new_record, 'gt').count():
                gt = filter_records(new_record, 'gt').earliest()
                new_record.end_date = datetime.datetime.strptime(str(gt.start_date), '%Y-%m-%d') - datetime.timedelta(
                    days=1)
                new_record.save(update_fields=['end_date'])

            return redirect(new_record)

        return render(request, 'exchange_rates/currency_create.html', context={'form': bound_form})
