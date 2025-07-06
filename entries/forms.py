from django import forms
from .models import Entry
from decimal import Decimal

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['date', 'amount', 'serial_number', 'weight', 'customer_name', 'given_by']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'step': '0.01'}),
        }

class InterestCalculationForm(forms.Form):
    RATE_CHOICES = [
        ('12', '12% (₹1 interest)'),
        ('13.8', '13.8% (₹1.15 interest)'),
        ('custom', 'Custom Rate')
    ]
    
    rate_type = forms.ChoiceField(
        choices=RATE_CHOICES,
        label='Interest Rate Type',
        widget=forms.RadioSelect
    )
    
    daily_rate = forms.DecimalField(
        max_digits=5,
        decimal_places=4,
        label='Daily Interest Rate (%)',
        min_value=Decimal('0'),
        max_value=Decimal('100'),
        required=False
    )
    
    to_date = forms.DateField(
        label='Calculate Interest Until',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        rate_type = cleaned_data.get('rate_type')
        daily_rate = cleaned_data.get('daily_rate')
        
        if rate_type == 'custom' and not daily_rate:
            raise forms.ValidationError('Please enter a custom daily rate')
            
        if rate_type != 'custom':
            # Convert annual rate to daily rate
            annual_rate = Decimal(rate_type)
            cleaned_data['daily_rate'] = round(annual_rate / Decimal('365'), 4)
            
        return cleaned_data

class EntryFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'All'),
        ('active', 'Active'),
        ('released', 'Released'),
        ('removed', 'Removed'),
    ]
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    customer_name = forms.CharField(required=False) 