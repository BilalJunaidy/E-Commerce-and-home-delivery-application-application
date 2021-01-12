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
    
    @property
    def get_item_total_quantity(self):
        orderitems = self.orderitem.all()
        total = sum([item.quantity for item in orderitems])
        return total 
    

    @property
    def get_item_total_amount(self):
        orderitems = self.orderitem.all()
        total = sum([item.get_item_total for item in orderitems])
        return total 

    @property
    def physical_product(self):
        orderitems = self.orderitem.all()
        physical_product = False
        for item in orderitems:

            # IMPORTANT TO REMEMBER AND TO KEEP A NOTE OF THIS
            # Initially the reason why this code was not working was because I was comparing the item.property.digital with the string 'False'
            # when I should have been comparing it with the boolean value of False since at this point in time, we are within the python environment 
            # and haven't converted our python boolean into Javascript strings. 
            if item.product.digital == False:
                physical_product = True
            
        return physical_product


        
        
        

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name = "orderitem")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default = 0, null=True, blank=True)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
    @property
    def get_item_total(self):
        total = self.product.price * self.quantity 
        return total 
    

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

    







