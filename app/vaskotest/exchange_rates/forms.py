from django import forms
from .models import ExchangeRate
from datetime import date


class ExchangeRateForm(forms.ModelForm):

    class Meta:
        model = ExchangeRate
        fields = ['currency', 'purchase', 'selling', 'start_date']

        widgets = {
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'purchase': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control'})
        }

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        if start_date and start_date > date.today():
            raise forms.ValidationError("'Start date' is in the future")

        return start_date

    def clean_purchase(self):
        purchase = self.cleaned_data.get('purchase')

        if purchase < 0:
            raise forms.ValidationError("'Purchase' can't be negative")

        return purchase

    def clean_selling(self):
        selling = self.cleaned_data.get('selling')

        if selling < 0:
            raise forms.ValidationError("'Selling' can't be negative")

        return selling

    def clean(self):
        cleaned_data = super().clean()
        purchase = cleaned_data.get('purchase')
        selling = cleaned_data.get('selling')

        if purchase and selling and purchase >= selling:
            raise forms.ValidationError("'Purchase' can't be greater than 'Selling'")


