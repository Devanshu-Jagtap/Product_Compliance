from django.urls import path
from .views import AdminRegisterView, CustomerRegisterView, EngineerRegisterView, LoginAPIView,ProfileAPIView,EngineerProfileCreateView,SpecializationListCreateView,SpecializationDetailView

urlpatterns = [
    path('register-admin/', AdminRegisterView.as_view(), name='register-admin'),
    path('register-customer/', CustomerRegisterView.as_view(), name='register-customer'),
    path('register-engineer/', EngineerRegisterView.as_view(), name='register-engineer'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/',ProfileAPIView.as_view(),name='profile'),
    path('profile/<int:pk>/',ProfileAPIView.as_view(),name='profile'),
    path('engineers/create/', EngineerProfileCreateView.as_view(), name='create-engineer'),
    path('specializations/', SpecializationListCreateView.as_view(), name='specialization-list-create'),
    path('specializations/<int:pk>/', SpecializationDetailView.as_view(), name='specialization-detail'),
]
