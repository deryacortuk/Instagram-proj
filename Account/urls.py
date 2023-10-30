from django.urls import path
from .views import sing_up, user_login, user_logout, activate, index,contact,about,pricing

app_name = "account"

urlpatterns = [
    path("", index, name="home"), 
    path("signup/", sing_up, name="signup"), 
    path("contact/", contact, name="contact"), 
     path("services/", about, name="about"), 
     path("pricing/", pricing, name="pricing"), 
    path("login/", user_login, name="login"), 
    path("logout/", user_logout, name="logout"), 
    path("activate/<uidb64>/<token>/", activate, name="activate"), 
    
    
]