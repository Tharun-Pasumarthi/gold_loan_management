from django.contrib import admin
from django.db.models import Sum, Count
from django.utils.html import format_html
from .models import Entry, AuditLog

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'customer_name', 'date', 'amount', 'weight', 'status', 'interest_rate', 'interest_amount', 'total_amount', 'user', 'created_at', 'updated_at')
    list_filter = ('status', 'date', 'user', 'created_at')
    search_fields = ('serial_number', 'customer_name', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    fieldsets = (
        ('Basic Information', {
            'fields': ('serial_number', 'customer_name', 'date', 'amount', 'weight', 'status')
        }),
        ('Interest Information', {
            'fields': ('interest_rate', 'interest_amount', 'total_amount')
        }),
        ('User Information', {
            'fields': ('user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-date', '-created_at')

    def total_amount(self, obj):
        return obj.amount + (obj.interest_amount or 0)
    total_amount.short_description = 'Total Amount'

    def changelist_view(self, request, extra_context=None):
        # Get statistics
        total_entries = Entry.objects.count()
        active_entries = Entry.objects.filter(status='active').count()
        released_entries = Entry.objects.filter(status='released').count()
        total_principal = Entry.objects.aggregate(total=Sum('amount'))['total'] or 0

        # Add statistics to the context
        extra_context = extra_context or {}
        extra_context['total_entries'] = total_entries
        extra_context['active_entries'] = active_entries
        extra_context['released_entries'] = released_entries
        extra_context['total_principal'] = total_principal

        return super().changelist_view(request, extra_context=extra_context)

    def interest_amount(self, obj):
        if obj.interest_amount:
            # Get the latest interest calculation from audit log
            latest_interest = AuditLog.objects.filter(
                entry=obj,
                action='calculate_interest'
            ).order_by('-timestamp').first()
            
            if latest_interest:
                return format_html(
                    '<span title="Last calculated on {}">{}</span>',
                    latest_interest.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    obj.interest_amount
                )
        return obj.interest_amount
    interest_amount.short_description = 'Interest Amount'

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'details')
    list_filter = ('action', 'user', 'timestamp')
    search_fields = ('user__username', 'action', 'details')
    readonly_fields = ('timestamp', 'user', 'action', 'details')
    ordering = ('-timestamp',)
