from django.test import TestCase
from django.urls import reverse
from .models import ExchangeRate
from datetime import date


class TestViews(TestCase):

    def setUp(self):
        """ Initial data """
        ExchangeRate.objects.create(currency='USD', purchase=24.45, selling=24.95,
                                    start_date='2019-12-30', end_date='2020-01-02')
        ExchangeRate.objects.create(currency='USD', purchase=24.15, selling=24.55,
                                    start_date='2020-01-03', end_date='2020-01-14')
        ExchangeRate.objects.create(currency='USD', purchase=24.15, selling=24.45,
                                    start_date='2020-01-15', end_date='2020-01-17')

    def test_add_record(self):
        """ Adding a course from today """
        before_add = ExchangeRate.objects.filter(currency='USD',
                                                 start_date=date.today()).exists()
        resp = self.client.post(reverse('currency_create_url'),
                                {'currency': 'USD', 'purchase': 25.15, 'selling': 25.45})
        after_add = ExchangeRate.objects.filter(currency='USD',
                                                start_date=date.today()).exists()

        self.assertFalse(before_add)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(after_add)

    def test_insert_record(self):
        """ Inserting course from a specific date """
        before_insert = ExchangeRate.objects.filter(currency='USD',
                                                    start_date='2020-01-10').exists()
        resp = self.client.post(reverse('currency_create_url'),
                                {'currency': 'USD', 'purchase': 24.75, 'selling': 25.15, 'start_date': '2020-01-10'})
        after_insert = ExchangeRate.objects.filter(currency='USD',
                                                   start_date='2020-01-10').exists()
        continuity = str(ExchangeRate.objects.get(currency='USD', start_date='2020-01-03').end_date)

        self.assertFalse(before_insert)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(after_insert)
        self.assertEqual(continuity, '2020-01-09')

    def test_delete_record(self):
        """ Deleting course valid from a specific date """
        before_delete = ExchangeRate.objects.filter(currency='USD', start_date='2020-01-03').exists()
        resp = self.client.post(reverse('delete_record_url',
                                        kwargs={'slug': 'USD', 'start_date': '2020-01-03'}))
        after_delete = ExchangeRate.objects.filter(currency='USD', start_date='2020-01-03').exists()
        continuity = str(ExchangeRate.objects.get(currency='USD', start_date='2019-12-30').end_date)

        self.assertTrue(before_delete)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(after_delete)
        self.assertEqual(continuity, '2020-01-14')
