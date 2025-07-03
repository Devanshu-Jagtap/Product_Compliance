from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer,ProfileSerializer,EngineerProfileSerializer,SpecializationSerializer
from ..utils.response import api_response
from rest_framework.permissions import IsAuthenticated
from .models import User,Profile,Specialization

class AdminRegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['role'] = 'admin'
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return api_response(message="Admin registered", data=serializer.data, code=status.HTTP_201_CREATED)
        return api_response(message="Failed", errors=serializer.errors, success=False, code=status.HTTP_400_BAD_REQUEST)

class CustomerRegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['role'] = 'customer'
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return api_response(message="Customer registered", data=serializer.data, code=status.HTTP_201_CREATED)
        return api_response(message="Failed", errors=serializer.errors, success=False, code=status.HTTP_400_BAD_REQUEST)

class EngineerRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'admin':
            return api_response(message="Only admin can create engineers", success=False, code=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['role'] = 'engineer'
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return api_response(message="Engineer registered", data=serializer.data, code=status.HTTP_201_CREATED)
        return api_response(message="Failed", errors=serializer.errors, success=False, code=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return api_response(
                message="Login successful",
                data=serializer.validated_data,
                code=status.HTTP_200_OK
            )
        return api_response(
            message="Invalid login credentials",
            success=False,
            errors=serializer.errors,
            code=status.HTTP_401_UNAUTHORIZED
        )
    
class ProfileAPIView(APIView):
    def post(self,request):
        serializer = ProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(message="Invalid Data",data=serializer.errors,success=False,code=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return api_response(message="Profile Created Successfully", data=serializer.data, code=status.HTTP_201_CREATED)

    def get(self,request,pk):
        try:
            user = Profile.objects.get(id=pk)
            serializer = ProfileSerializer(user)
            return api_response(message="Data",data=serializer.data,code=status.HTTP_200_OK)
        except User.DoesNotExist:
            return api_response(message="User Does Not Exist",data=None,success=False,code=status.HTTP_400_BAD_REQUEST)

class EngineerProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = EngineerProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(message="Invalid data", data=serializer.errors, success=False, code=status.HTTP_400_BAD_REQUEST)

        profile = serializer.save()
        return api_response(
            message="Engineer profile created successfully",
            data=EngineerProfileSerializer(profile).data,
            code=status.HTTP_201_CREATED
        )

class SpecializationListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Specialization.objects.all().order_by('name')
        serializer = SpecializationSerializer(queryset, many=True)
        return api_response(
            message="Specialization list",
            data=serializer.data,
            code=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = SpecializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Specialization created successfully",
                data=serializer.data,
                code=status.HTTP_201_CREATED
            )
        return api_response(
            message="Invalid data",
            data=serializer.errors,
            success=False,
            code=status.HTTP_400_BAD_REQUEST
        )

class SpecializationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Specialization.objects.get(pk=pk)
        except Specialization.DoesNotExist:
            return None

    def get(self, request, pk):
        specialization = self.get_object(pk)
        if not specialization:
            return api_response("Specialization not found", success=False, code=404)

        serializer = SpecializationSerializer(specialization)
        return api_response("Specialization detail", serializer.data, code=200)

    def put(self, request, pk):
        specialization = self.get_object(pk)
        if not specialization:
            return api_response("Specialization not found", success=False, code=404)

        serializer = SpecializationSerializer(specialization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response("Updated successfully", serializer.data, code=200)

        return api_response("Invalid data", serializer.errors, success=False, code=400)

    def delete(self, request, pk):
        specialization = self.get_object(pk)
        if not specialization:
            return api_response("Specialization not found", success=False, code=404)

        specialization.delete()
        return api_response("Deleted successfully", data=None, code=204)
