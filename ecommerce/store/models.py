from django.db import models
from django.contrib.auth.models import User 
from PIL import Image

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=False, on_delete = models.CASCADE)
    name = models.CharField(max_length = 255, null=True)
    email = models.EmailField(max_length = 255, null=True)

    def __str__(self):
        return self.name 

class Product(models.Model):
    name = models.CharField(max_length = 255)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to = 'Product_Images')

    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True) 
    completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length = 100, null=True)

    def __str__(self):
        return str(self.id) 
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default = 0, null=True, blank=True)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    

class ShippingAddress(models.Model):
    address = models.CharField(max_length=255, blank=False, null=False)
    country = models.CharField(max_length=255, blank=False, null=False)
    city = models.CharField(max_length=255, blank=False, null=False)
    state = models.CharField(max_length=255, blank=False, null=False)
    zip_code = models.CharField(max_length=255, blank=False, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) 
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    







