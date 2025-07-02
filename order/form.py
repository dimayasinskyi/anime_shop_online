from django import forms
from .models import Order


class CheckCorrectOrderForm(forms.ModelForm):
    city = forms.CharField()
    address = forms.CharField()
    state = forms.CharField()
    zip = forms.CharField()


    class Meta:
        model = Order
        fields = ['city','address', 'state', 'zip',]
        exclude = ['create_time', 'paid']