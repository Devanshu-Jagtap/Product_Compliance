from apps.users.base_models import *
from apps.users.models import User

class ChatMessage(BaseContent):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.email} to {self.receiver.email}"

class Notification(BaseContent):  
    NOTIFICATION_TYPES = [
        ('info', 'Info'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('alert', 'Alert'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    

    def __str__(self):
        return f"Notification to {self.recipient.email} - {self.title}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()