# users/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models
from apps.users.base_models import *

from django.apps import apps
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('engineer', 'Engineer'),
        ('customer', 'Customer'),
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    def __str__(self):
        return f"{self.full_name} ({self.role})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Specialization(BaseContent):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Profile(BaseContent):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_image/", blank=True, null=True)
    id_proof = models.FileField(upload_to="id_proofs/", blank=True, null=True)
    # For engineers
    is_available = models.BooleanField(default=True) 
    max_capacity = models.IntegerField(default=5)
    specializations = models.ManyToManyField(Specialization, blank=True) 

    def __str__(self):
        return f"Profile of {self.user.email}"
    def is_engineer(self):
        return self.user.role == 'engineer'
    