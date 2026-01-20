from django.contrib import admin
from .models import Thread, Message

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'coach', 'job_post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['vendor__organization_name', 'coach__display_name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['thread', 'sender', 'sender_type', 'created_at']
    list_filter = ['sender_type', 'created_at']
    search_fields = ['body', 'sender__username']
