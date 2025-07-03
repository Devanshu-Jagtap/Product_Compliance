from rest_framework import serializers
from .models import Claim,User,Issue,EngineerTask

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'product', 'specialization_required', 'issue_rating', 'min_day']

    def validate_issue_rating(self, value):
        if not (0 < value < 10):
            raise serializers.ValidationError("Issue rating must be between 1 and 9.")
        return value
    
class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'

    def validate_customer(self,customer):
        try:
            User.objects.get(id=customer.id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        return customer
    
    def create(self,validated_data):
        customer = validated_data.pop("customer")
        return Claim.objects.create(customer=customer,**validated_data)

class EngineerTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineerTask
        fields = ['id', 'is_resolved', 'resolution_note', 'resolution_file']
        read_only_fields = ['id']

    def validate(self, data):
        if data.get('is_resolved') and not data.get('resolution_note'):
            raise serializers.ValidationError("Please provide a resolution note when marking as resolved.")
        return data
    
class EngineerTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineerTask
        fields = ['id', 'is_resolved', 'resolution_note', 'resolution_file']
        read_only_fields = ['id']

    def validate(self, data):
        if data.get('is_resolved') and not data.get('resolution_note'):
            raise serializers.ValidationError("Please provide a resolution note when marking as resolved.")
        return data