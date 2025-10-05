# forms.py
from django import forms
from .models import *

# return request for return page logic
class ReturnRequestForm(forms.Form):
    ORDER_NUMBER_HELP_TEXT = "Enter your order number as it appears on your confirmation email"
    EMAIL_HELP_TEXT = "Enter the email address you used when placing the order"
    
    RETURN_TYPE_CHOICES = [
        ('refund', 'Return for Refund'),
        ('size_exchange', 'Exchange for Different Size'),
        ('color_exchange', 'Exchange for Different Color'),
    ]
    
    order_number = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary',
            'placeholder': 'e.g. MJ2023456'
        }),
        help_text=ORDER_NUMBER_HELP_TEXT
    )
    
    customer_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary',
            'placeholder': 'your@email.com'
        }),
        help_text=EMAIL_HELP_TEXT
    )
    
    return_type = forms.ChoiceField(
        choices=RETURN_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'focus:ring-primary h-4 w-4 text-primary border-gray-300'
        })
    )
    
    reason = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary'
        })
    )
    
    additional_details = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary',
            'rows': 4,
            'placeholder': 'Please provide any additional information about your return'
        })
    )
    
    agreed_to_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'focus:ring-primary h-4 w-4 text-primary border-gray-300 rounded'
        })
    )
    
    def __init__(self, *args, **kwargs):
        return_reasons = kwargs.pop('return_reasons', None)
        super().__init__(*args, **kwargs)
        
        if return_reasons:
            reason_choices = [('', 'Select a reason')] + [
                (reason.reason, reason.reason) for reason in return_reasons
            ]
            self.fields['reason'].choices = reason_choices


# product checkout forms

class CheckoutForm(forms.Form):
    shipping_full_name = forms.CharField(
        max_length=200, 
        required=True,
        label="Full Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'})
    )
    shipping_email = forms.EmailField(required=True)
    shipping_phone = forms.CharField(max_length=15, required=True)
    shipping_address = forms.CharField(widget=forms.Textarea, required=True)
    shipping_city = forms.CharField(max_length=100, required=True)
    shipping_state = forms.CharField(max_length=100, required=False)
    shipping_zip_code = forms.CharField(max_length=10, required=False)
    delivery_area = forms.ChoiceField(choices=[('inside', 'Inside Dhaka'), ('outside', 'Outside Dhaka')], required=True)
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_METHOD_CHOICES, required=True)
    transaction_id = forms.CharField(max_length=100, required=False)
    sender_mobile_number = forms.CharField(max_length=15, required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False)
