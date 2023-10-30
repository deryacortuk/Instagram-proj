from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
        
    def __str__(self) -> str:
        return self.user.get_full_name()
    
    
class UserSearch(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_search")
    instagram_user = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ('-updated_at',)
        
    
    def __str__(self):
        return self.instagram_user
    
    def get_absolute_url(self):
        return reverse('userhub:analysis', args=[self.instagram_user])
    
class SearchServiceCount(models.Model):
    STATUS_CHOICES = (
    ('basic','Basic'),('premium','Premium'),('pro','Pro')
)  

    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="search_service")
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default='basic',max_length=100)
    class Meta:
        ordering = ('-updated_at',)
    def __str__(self) -> str:
       return self.user.username
    
    
    