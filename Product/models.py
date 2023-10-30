from django.db import models
from datetime import datetime, timedelta
import uuid



class ServiceProduct(models.Model):
    STATUS_CHOICES = (('premium','Premium'),('pro','Pro'))  
    name = models.CharField(max_length=255, db_index=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True, db_index=True)         
    category = models.CharField(max_length=20, choices=STATUS_CHOICES)    
    quantity = models.IntegerField(default=0)
    
 

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name', 'available']),  
        ]

   