# issue/urls.py
from django.urls import path
from apps.claims.views import IssueListCreateView, IssueDetailView,EngineerTaskUpdateView,ClaimCreateAPIView
from apps.communication.notification import *

urlpatterns = [
    path('issues/', IssueListCreateView.as_view(), name='issue-list-create'),
    path('issues/<int:pk>/', IssueDetailView.as_view(), name='issue-detail'),
    path('claims/', ClaimCreateAPIView.as_view(), name='assign-engineer'),
    path('tasks/<int:pk>/update/', EngineerTaskUpdateView.as_view(), name='update-task'),
    
]
