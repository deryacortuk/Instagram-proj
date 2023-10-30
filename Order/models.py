from django.db import models
import uuid
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from Product.models import ServiceProduct
from UserHub.models import SearchServiceCount



class Order(models.Model):
    STATUS_CHOICES = (
    ('created','Created'),('paid','Paid'),('delivered','delivered'),('refunded','refunded')
)  

    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_user")           
    stripe_id = models.CharField(max_length=250, blank=True)
    active = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)        
    status = models.CharField(choices=STATUS_CHOICES, default='created',max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)        
    updated_at = models.DateTimeField(auto_now=True)      
    
    
    class Meta:
        ordering = ('-created_at',)
        
    
    def __str__(self):
        return str(self.id)      
    
 
   
    
    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '__test__' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f"https://dashoard.stripe.com{path}payments/{self.stripe_id}"
    

class OrderItem(models.Model):
    order= models.ForeignKey(Order,related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(ServiceProduct, related_name="order_items",on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    
    def __str__(self):
        return str(self.id)
    