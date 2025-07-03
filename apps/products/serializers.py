from rest_framework import serializers
from .models import ProductCategory,Product,CustomerProduct,ProductRecall

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        models = ProductCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProduct
        fields = '__all__'
        read_only_fields = ['customer']  # we set this from backend

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)
    
class ProductFilterSerializer(serializers.Serializer):
    category = serializers.IntegerField(required=False)
    manufacturer_id = serializers.IntegerField(required=False)

class ProductRecallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRecall
        fields = '__all__'


