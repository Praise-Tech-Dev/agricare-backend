from django.contrib import admin
from .models import Farmer, Conversation, HealthCase

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'name', 'flock_size', 'created_at')
    search_fields = ('phone_number', 'name')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'sender_type', 'timestamp')
    list_filter = ('sender_type',)

@admin.register(HealthCase)
class HealthCaseAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'status', 'severity_score', 'created_at')
    list_filter = ('status',)
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='Resolved')
