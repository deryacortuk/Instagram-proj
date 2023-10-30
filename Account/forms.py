from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

def email_validation(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError((f"{email} is used!"), params={"value":email})
    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(validators=[email_validation])
    
    class Meta:
        model = User 
        fields = ["first_name","last_name","username","email","password1","password2"]
        
class LoginForm(forms.Form):
    username = forms.CharField(label="email or username")
    password = forms.CharField(widget=forms.PasswordInput)
    