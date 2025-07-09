
from apps.users.models import Profile
from apps.claims.models import EngineerTask
from django.db.models import Q, Count

# def assign_engineer_to_claim(claim):
#     required_specialization = claim.issue.specialization_required

#     engineers = Profile.objects.filter(
#         user__role='engineer',
#         is_available=True,
#         specializations__in=[required_specialization]
#     ).annotate(
#         task_count=Count('user__engineertask', filter=Q(user__engineertask__is_resolved=False))
#     ).order_by('task_count')

#     if not engineers.exists():
#         return None 

#     selected_engineer = engineers.first()

#     EngineerTask.objects.create(
#         engineer=selected_engineer.user,
#         claim=claim
#     )

#     return selected_engineer.user

def assign_engineer_to_claim(claim):
    required_specialization = claim.issue.specialization_required
    print(f"Required Specialization: {required_specialization} (ID: {required_specialization.id})")

    engineers_qs = Profile.objects.filter(
        user__role='engineer',
        is_available=True,
        specializations__in=[required_specialization]
    )

    print(f" Engineers matching specialization: {[e.user.email for e in engineers_qs]}")

    engineers = engineers_qs.annotate(
        task_count=Count('user__engineertask', filter=Q(user__engineertask__is_resolved=False))
    ).order_by('task_count')

    if not engineers.exists():
        print("No engineers found with required specialization and availability.")
        return None

    selected_engineer = engineers.first()
    print(f"Selected engineer: {selected_engineer.user.email} with task count: {selected_engineer.task_count}")

    try:
        task = EngineerTask.objects.create(
            engineer=selected_engineer.user,
            claim=claim
        )
        print(f"🆕 EngineerTask created with ID: {task.id} for claim ID: {claim.id}")
    except Exception as e:
        print(f"Failed to create EngineerTask: {e}")
        return None

    return selected_engineer.user

