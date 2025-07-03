# claims/models.py
from apps.users.base_models import *
from apps.users.models import User,Specialization
from apps.products.models import *
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

class Issue(BaseContent):
    title = models.CharField(max_length=255)
    product = models.CharField(max_length=100)
    specialization_required = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    issue_rating = models.IntegerField()
    min_day = models.IntegerField()

    def __str__(self):
            return self.title
    def clean(self):
        if not (0 < self.issue_rating < 10):
                raise ValidationError({'issue_rating': 'Issue rating must be between 1 and 9.'})

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
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    recall = models.ForeignKey(ProductRecall, on_delete=models.SET_NULL, null=True, blank=True)
    claim_type = models.CharField(max_length=20, choices=CLAIM_TYPE_CHOICES, default='general')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority_score = models.IntegerField(default=0)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Claim #{self.id} by {self.customer.email}"
    
    def save(self, *args, **kwargs):
        if self.issue:
            self.priority_score = self.issue.issue_rating
            if not self.due_date:
                self.due_date = timezone.now().date() + timedelta(days=self.issue.min_day)
        super().save(*args, **kwargs)

class ClaimImage(BaseContent):
    claim = models.ForeignKey(Claim,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="claims/", null=True, blank=True)

    def __str__(self):
        return f"Image for Claim #{self.claim.id}"
    
class EngineerTask(BaseContent):
    engineer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'engineer'})
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE,related_name='tasks')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolution_note = models.TextField(null=True, blank=True)
    resolution_file = models.FileField(upload_to="task_reports/", null=True, blank=True)

    def __str__(self):
        return f"Task for claim #{self.claim.id} - Engineer: {self.engineer.name}"
