from django.urls import path
from .views import sing_up, user_login,policy_privacy,faq, user_logout, activate, index,contact,about,pricing,sample_analyze_user

app_name = "account"

urlpatterns = [
    path("", index, name="home"), 
    path("signup/", sing_up, name="signup"), 
    path("contact/", contact, name="contact"), 
     path("services/", about, name="about"), 
     path("faq/",faq, name="faq"), 
     path("pricing/", pricing, name="pricing"), 
    path("login/", user_login, name="login"), 
    path("logout/", user_logout, name="logout"), 
     path("privacy-policy/", policy_privacy, name="policy"), 
    path("activate/<uidb64>/<token>/", activate, name="activate"), 
    path("sample/davidbeckham/", sample_analyze_user, name="sample_user"), 
    
    
]