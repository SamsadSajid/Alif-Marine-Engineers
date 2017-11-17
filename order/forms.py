from django import forms
from .models import Order
from phonenumber_field.formfields import PhoneNumberField


class OrderCreateForm(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': '+8801XXXXXXXXX'}), label="Phone number",
                             required=False)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'zip', 'city']