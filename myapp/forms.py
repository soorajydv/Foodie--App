from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["shipping_address",
                  "mobile", "email", "payment_method"]
