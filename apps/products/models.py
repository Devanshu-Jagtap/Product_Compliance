# products/models.py
from apps.users.base_models import *
from apps.users.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_image = models.ImageField(upload_to="product_image/", blank=True, null=True)
    name = models.CharField(max_length=255)
    model_number = models.CharField(max_length=100, unique=True)
    manufacturer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name="products")

    def __str__(self):
        return self.name

class CustomerProduct(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'},related_name="product_orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100)
    purchase_date = models.DateField()
    invoice_file = models.FileField(upload_to="invoices/", null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} owned by {self.customer.email}"
    
class ProductRecall(BaseContent):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="products_recall")
    initiated_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})
    reason = models.TextField()
    date_initiated = models.DateField(auto_now_add=True)
    resolution_steps = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Recall for {self.product.name}"