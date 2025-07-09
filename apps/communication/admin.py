from django.contrib import admin
from .models import ChatMessage, Notification

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'message_preview', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['sender__email', 'receiver__email', 'message']
    autocomplete_fields = ['sender', 'receiver']

    def message_preview(self, obj):
        return obj.message[:50] + ("..." if len(obj.message) > 50 else "")
    message_preview.short_description = 'Message'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipient', 'title', 'notification_type', 'is_read']
    list_filter = ['notification_type', 'is_read']
    search_fields = ['title', 'recipient__email', 'sender__email']
    autocomplete_fields = ['sender', 'recipient']
