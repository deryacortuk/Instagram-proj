from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .token import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.cache import never_cache
from django.contrib import messages
import logging
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import JsonResponse
from UserHub.tasks import get_instagram_task
from UserHub.models import UserSearch, SearchServiceCount
from django.http import JsonResponse
from UserHub.tasks import get_instagram_task


logger = logging.getLogger(__name__)

def index(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username')
            search = SearchServiceCount.objects.filter(user=request.user).first()
            if search.quantity > 0:
                user = request.user.username
                get_instagram_task.delay(username,user)                          
                message = f"When {username}'s Instagram profile analysis is completed, you will be notified by e-mail and the analysis result will be on your analysis list page. Thank you for your patient. "
             
        
                return render(request,"userhub/discovery.html",{"message":message})
            return JsonResponse({"result":"Please upgrade your account"})
        
        return render(request, "userhub/discovery.html")
    return render(request,"index.html")

def pricing(request):
    return render(request,"pricing.html")


def sing_up(request):
    form = RegisterForm()
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        to_email = request.POST.get("email")
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            current_site = get_current_site(request).domain
            subject = "X website Activation Your Account"
            
            message = render_to_string('account/activation/activation_account_email.html',{
                "user":user, "domain":current_site, "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                "token":account_activation_token.make_token(user)
            })
            
            send_mail(subject, message,"sellorbuy@sellorbuy.shop",[to_email], fail_silently=False)
            
            return render(request,"account/activation/activation_email_sent.html",{"user":user})
        else:
            return render(request, "account/signup.html",{"form":form})
    return render(request, "account/signup.html",{"form":form})


def activate(request, uidb64, token, backend="django.contrib.auth.backends.ModelBackend"):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        return render(request, "account/activation/activation_email_success.html")
    return render(request,"account/activation/activation_email_invalid.html")

def user_login(request):
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    logger.info(REDIRECT_FIELD_NAME)
                    login(request, user)
                    return redirect("account:home")
                else:
                    messages.info(request,"Please activate your account.Activation mail was sent.")
            else:
                messages.info(request,"Please check your information!")
    return render(request, "account/login.html",{"form":form})

@never_cache
def user_logout(request):
    logout(request)
    return redirect("account:home")

def about(request):   
    return render(request, "about.html")

from django.core.mail import send_mail

def contact(request):
   
    if request.method == "POST":
        message_name = request.POST['name']
        message_email = request.POST['email']
        message_content = request.POST['content']
        
        email_send = EmailMessage(
        subject=message_name, 
        body=message_content, 
        from_email='sellorbuy@sellorbuy.shop',  
        to=['sellorbuy@sellorbuy.shop'],
        reply_to=[message_email])     
        
        email_send.send()
        message = "Thank you for contacting us. We will contact you very soon! "
        return render(request, 'contact.html',{'message':message})
        
    return render(request,'contact.html')

    

def handler_not_found(request,exception):
    
    return render(request,'404.html')

def handler_server_error(request):
    
    return render(request,'500.html')


    
def handler_400(request,exception):
    
    return render(request, '400.html')

def handler403(request,exception):
    
    return render(request, '403.html')