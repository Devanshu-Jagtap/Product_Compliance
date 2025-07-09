from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import Profile,Specialization

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'role', 'password', 'confirm_password']

        extra_kwargs = {
            'role': {'required': False}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive")
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'email': user.email,
            'role': user.role,
            'full_name': user.full_name
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def validate_user(self,value):
        try:
            User.objects.get(id=value.id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        return value
    
    def create(self, validated_data):
        user = validated_data.pop('user')
        specializations = validated_data.pop('specializations', [])
        profile = Profile.objects.create(user=user, **validated_data)
        profile.specializations.set(specializations)
        return profile
    
class EngineerProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ['email', 'password', 'full_name', 'phone_number', 'address', 'profile_image', 'id_proof', 'specializations', 'is_available', 'max_capacity']

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "User with this email already exists."})
        return data

    def create(self, validated_data):
        # Extract and pop user-related fields
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        full_name = validated_data.pop('full_name')

        # Create the User with role = engineer
        user = User.objects.create_user(
            email=email,
            password=password,
            role='engineer',  # hardcoded safely
            full_name=full_name
        )

        # Create the profile
        profile = Profile.objects.create(user=user, **validated_data)
        profile.specializations.set(validated_data.get('specializations', []))
        return profile
    
class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name']