# claim/services.py
from users.models import Profile
from .models import EngineerTask
from django.db.models import Q, Count

def assign_engineer_to_claim(claim):
    required_specialization = claim.issue.specialization_required

    engineers = Profile.objects.filter(
        user__role='engineer',
        is_available=True,
        specializations=required_specialization
    ).annotate(
        task_count=Count('user__engineertask', filter=Q(user__engineertask__is_resolved=False))
    ).order_by('task_count')

    if not engineers.exists():
        return None  # Or log as unassigned

    selected_engineer = engineers.first()

    EngineerTask.objects.create(
        engineer=selected_engineer.user,
        claim=claim
    )

    return selected_engineer.user
