from django import forms
from .models import ShippingLabel

class ShippingLabelForm(forms.ModelForm):
    class Meta:
        model = ShippingLabel
        exclude = ['tracking_id', 'barcode_image', 'status','pdf_file']
        widgets = {
            'sender_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sender Name'}),
            'sender_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Sender Address', 'rows': 3}),
            'receiver_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receiver Name'}),
            'receiver_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Receiver Address', 'rows': 3}),
            'origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Origin'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination'}),
            'actual_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (kg)', 'step': '0.01'}),
            'chargable_weight': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Weight (kg)',}),
            'number_of_box':forms.NumberInput(attrs={'class': 'form-control','placeholder':'box' }),
            'service':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'remarks', 'rows': 3}),
            # Add other fields similarly if needed
        }
        
        
class LoginForm(forms.Form):
    
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
