from django.contrib import admin
from .models import Issue, Claim, ClaimImage, EngineerTask

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'specialization_required', 'issue_rating', 'min_day']
    search_fields = ['title', 'product']
    list_filter = ['specialization_required']


class ClaimImageInline(admin.TabularInline):
    model = ClaimImage
    extra = 1


class EngineerTaskInline(admin.TabularInline):
    model = EngineerTask
    extra = 1
    fields = ['engineer', 'is_resolved', 'resolution_note', 'resolution_file']
    autocomplete_fields = ['engineer']


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['id', 'issue', 'customer', 'claim_type', 'status', 'priority_score', 'due_date']
    list_filter = ['status', 'claim_type']
    search_fields = ['customer__email', 'issue__title']
    autocomplete_fields = ['customer', 'issue', 'recall']
    inlines = [ClaimImageInline, EngineerTaskInline]


@admin.register(ClaimImage)
class ClaimImageAdmin(admin.ModelAdmin):
    list_display = ['claim', 'image']


@admin.register(EngineerTask)
class EngineerTaskAdmin(admin.ModelAdmin):
    list_display = ['claim', 'engineer', 'assigned_at', 'is_resolved']
    list_filter = ['is_resolved']
    search_fields = ['claim__id', 'engineer__email']
    autocomplete_fields = ['claim', 'engineer']
