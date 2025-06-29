# claims/models.py
from apps.users.base_models import *
from apps.users.models import User
from apps.products.models import *

class Claim(BaseContent):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    )

    CLAIM_TYPE_CHOICES = (
        ('recall', 'Recall'),
        ('general', 'General')
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    recall = models.ForeignKey(ProductRecall, on_delete=models.SET_NULL, null=True, blank=True)
    claim_type = models.CharField(max_length=20, choices=CLAIM_TYPE_CHOICES, default='general')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    def __str__(self):
        return f"Claim #{self.id} by {self.customer.email}"

class ClaimImage(BaseContent):
    claim = models.ForeignKey(Claim,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="claims/", null=True, blank=True)

    def __str__(self):
        return f"Image for Claim #{self.claim.id}"
    
class EngineerTask(BaseContent):
    engineer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'engineer'})
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolution_note = models.TextField(null=True, blank=True)
    resolution_file = models.FileField(upload_to="task_reports/", null=True, blank=True)

    def __str__(self):
        return f"Task for claim #{self.claim.id} - Engineer: {self.engineer.name}"
