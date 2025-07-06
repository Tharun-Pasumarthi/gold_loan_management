from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User

class Entry(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('released', 'Released'),
        ('removed', 'Removed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    from_date = models.DateField(editable=False)  # Will be set to date automatically
    to_date = models.DateField(null=True, blank=True)
    serial_number = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight in grams")
    given_by = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    released_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Always set from_date to the entry's date
        self.from_date = self.date
        super().save(*args, **kwargs)

    def calculate_interest(self, daily_rate):
        if not self.to_date:
            self.to_date = timezone.now().date()
        
        days = (self.to_date - self.from_date).days
        
        # Minimum 15 days interest
        if days < 15:
            days = 15
            
        # Convert daily rate to decimal
        daily_rate_decimal = Decimal(str(daily_rate)) / Decimal('100')
        days_decimal = Decimal(str(days))
        
        if days >= 365:
            # Compound interest for periods >= 365 days
            # For 12% annual rate: daily rate = 12/365 = 0.03288%
            # For 13.8% annual rate: daily rate = 13.8/365 = 0.03781%
            interest = self.amount * ((Decimal('1') + daily_rate_decimal) ** days_decimal - Decimal('1'))
        else:
            # Simple interest for periods < 365 days
            # For 12% annual rate: daily rate = 12/365 = 0.03288%
            # For 13.8% annual rate: daily rate = 13.8/365 = 0.03781%
            interest = self.amount * daily_rate_decimal * days_decimal
            
        # Round to 2 decimal places
        return round(interest, 2)

    @classmethod
    def get_daily_rate(cls, annual_rate):
        """
        Convert annual rate to daily rate
        """
        return round(Decimal(str(annual_rate)) / Decimal('365'), 4)  # Round to 4 decimal places

    def release(self):
        """Mark the entry as released"""
        self.status = 'released'
        self.released_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.serial_number} - {self.customer_name}"

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('edit', 'Edit'),
        ('calculate_interest', 'Calculate Interest'),
        ('release', 'Release'),
    ]

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user} on {self.entry}"
