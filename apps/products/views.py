from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .models import ProductCategory,Product,CustomerProduct,ProductRecall
from .serializers import ProductCategorySerializer,ProductSerializer,CustomerProductSerializer,ProductFilterSerializer,ProductRecallSerializer
from apps.utils.response import api_response
from apps.utils.permissions import IsAdminOrReadOnly,IsCustomerOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
# Create your views here.

class ProductCategoryListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        categories = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)
        return api_response({
            "message": "Category list fetched successfully",
            "data": serializer.data,
            "status": "success",
            "code": status.HTTP_200_OK
        })

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message ="Category created successfully",
                data=serializer.data,
                code=status.HTTP_201_CREATED
            )
        return api_response(
            message= "Creation failed",
            errors= serializer.errors,
            status=False,
            code= status.HTTP_400_BAD_REQUEST
        )

class ProductCategoryDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(ProductCategory, pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = ProductCategorySerializer(category)
        return api_response(
            message="Category fetched successfully",
            data= serializer.data,
            code=status.HTTP_200_OK
        )

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = ProductCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message= "Category updated",
                data=serializer.data,
                code= status.HTTP_200_OK
            )
        return api_response(
            message= "Update failed",
            errors=serializer.errors,
            status= False,
            code= status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return api_response(
            message= "Category deleted",
            code= status.HTTP_204_NO_CONTENT
        )
    
class ProductListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return api_response(
            message="Product list fetched successfully",
            data=serializer.data
        )

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Product created successfully",
                data=serializer.data,
                code=status.HTTP_201_CREATED
            )
        return api_response(
            message="Validation failed",
            errors=serializer.errors,
            success=False,
            code=status.HTTP_400_BAD_REQUEST
        )

class ProductDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return api_response(
            message="Product details fetched",
            data=serializer.data
        )

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Product updated successfully",
                data=serializer.data
            )
        return api_response(
            message="Update failed",
            errors=serializer.errors,
            success=False,
            code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return api_response(
            message="Product deleted successfully",
            code=status.HTTP_204_NO_CONTENT,
            data=None
        )

class CustomerProductListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomerOwnerOrReadOnly]

    def get(self, request):
        products = CustomerProduct.objects.all()
        serializer = CustomerProductSerializer(products, many=True)
        return api_response(message="Customer products fetched", data=serializer.data)

    def post(self, request):
        serializer = CustomerProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return api_response(message="Product added successfully", data=serializer.data, code=201)
        return api_response(message="Failed to add product", errors=serializer.errors, success=False, code=400)


class CustomerProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomerOwnerOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(CustomerProduct, pk=pk)

    def get(self, request, pk):
        obj = self.get_object(pk)
        self.check_object_permissions(request, obj)
        serializer = CustomerProductSerializer(obj)
        return api_response(message="Product details", data=serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        self.check_object_permissions(request, obj)
        serializer = CustomerProductSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return api_response(message="Product updated", data=serializer.data)
        return api_response(message="Update failed", errors=serializer.errors, success=False, code=400)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        self.check_object_permissions(request, obj)
        obj.delete()
        return api_response(message="Product deleted", data=None, code=204)
    
class ProductFilterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = ProductFilterSerializer(data=request.query_params)
        if not serializer.is_valid():
            return api_response(message='Invalid input',errors=serializer.errors, success=False,code=status.HTTP_400_BAD_REQUEST)
        
        filters= serializer.validated_data
        queryset = Product.objects.all()

        if 'category' in filters:
            queryset = queryset.filter(category__iexact=filters['category'])

        if 'manufacturer_id' in filters:
            queryset = queryset.filter(manufacturer_id=filters['manufacturer_id'])

class ProductRecallAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ProductRecallSerializer(data=request.data)

        if not serializer.is_valid():
            return api_response(message="Invalid input", errors=serializer.errors, success=False,code=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return api_response(message="Products recall created successfully", data=serializer.data,code=status.HTTP_201_CREATED)
    
    def get(self,request,pk):
        if not pk:
            recalls = ProductRecall.objects.all()
            serializer = ProductRecallSerializer(recalls,many=True)
            return api_response(message="Product Recall All",data=serializer.data,code=status.HTTP_200_OK)
        else:
            try:
                recall = ProductRecall.objects.get(id=pk)
            except ProductRecall.DoesNotExist:
                return api_response(
                    message="Recall does not exist",
                    data=None,
                    success=False,
                    code=status.HTTP_404_NOT_FOUND
                )
            if not recalls:
                return api_response(message="Recall Does Not exists",data=None,success=False,code=status.HTTP_400_BAD_REQUEST)
            
            serializer = ProductRecallSerializer(recalls)
            return api_response(message="Product Recall All",data=serializer.data,code=status.HTTP_200_OK)
