from datetime import date
from django.db import models
from django.core.validators import MinLengthValidator
from django.shortcuts import reverse


CURRENCIES = ('UAN', 'Ukrainian hryvnia'), ('USD', 'Dollar'), ('EUR', 'Euro'), ('RUB', 'Russian ruble')


class ExchangeRate(models.Model):
    """ A model that represents currency exchange rates """

    currency = models.CharField(
        choices=CURRENCIES,
        default=CURRENCIES[1][0],
        max_length=3,
        validators=[MinLengthValidator(3)]
    )

    purchase = models.FloatField()
    selling = models.FloatField()
    start_date = models.DateField(blank=True, default=date.today)
    end_date = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('currency_history_url', kwargs={'slug': self.currency})

    class Meta:
        ordering = ['start_date']
        get_latest_by = 'start_date'

    def __str__(self):
        return '{}, start_date: {}'.format(self.currency, self.start_date)

    def save(self, *args, **kwargs):
        if ExchangeRate.objects.filter(currency=self.currency, start_date=self.start_date).count():
            new_record = ExchangeRate.objects.get(currency=self.currency, start_date=self.start_date)
            self.id = new_record.id
        super().save(*args, **kwargs)



