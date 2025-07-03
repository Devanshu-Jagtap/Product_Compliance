from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ClaimSerializer,IssueSerializer,EngineerTaskUpdateSerializer
from utils.response import api_response
from .models import Issue,EngineerTask
from rest_framework.permissions import IsAuthenticated
from .service import assign_engineer_to_claim 

# Create your views here.
class IssueListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Issue.objects.all().order_by('-id')
        serializer = IssueSerializer(queryset, many=True)
        return api_response("Issue list", serializer.data, code=200)

    def post(self, request):
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response("Issue created successfully", serializer.data, code=201)
        return api_response("Invalid data", serializer.errors, success=False, code=400)

class IssueDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Issue.objects.get(pk=pk)
        except Issue.DoesNotExist:
            return None

    def get(self, request, pk):
        issue = self.get_object(pk)
        if not issue:
            return api_response("Issue not found", success=False, code=404)
        serializer = IssueSerializer(issue)
        return api_response("Issue details", serializer.data)

    def put(self, request, pk):
        issue = self.get_object(pk)
        if not issue:
            return api_response("Issue not found", success=False, code=404)

        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response("Updated successfully", serializer.data)
        return api_response("Invalid data", serializer.errors, success=False, code=400)

    def delete(self, request, pk):
        issue = self.get_object(pk)
        if not issue:
            return api_response("Issue not found", success=False, code=404)
        issue.delete()
        return api_response("Deleted successfully", None, code=204)

class ClaimCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ClaimSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return api_response("Invalid data", serializer.errors, success=False, code=400)

        claim = serializer.save(customer=request.user)

        # 👇 Auto assign after claim is saved
        assigned_engineer = assign_engineer_to_claim(claim)

        message = "Claim created successfully"
        if assigned_engineer:
            message += f" and assigned to {assigned_engineer.email}"
        else:
            message += " but no engineer available now"

        return api_response(message, serializer.data, code=201)
    
class EngineerTaskUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            task = EngineerTask.objects.get(pk=pk, engineer=request.user)
        except EngineerTask.DoesNotExist:
            return api_response("Task not found or not assigned to you", success=False, code=404)

        serializer = EngineerTaskUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            claim = task.claim
            tasks = claim.tasks.all()

            if all(t.is_resolved for t in tasks):
                claim.status = 'resolved'
            elif any(t.is_resolved for t in tasks):
                claim.status = 'in_progress'
            else:
                claim.status = 'open'

            claim.save()

            return api_response("Task updated successfully", serializer.data, code=200)

        return api_response("Invalid data", serializer.errors, success=False, code=400)
