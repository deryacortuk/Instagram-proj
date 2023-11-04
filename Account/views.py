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
from UserHub.tasks import get_instagram_task
from UserHub.models import UserSearch, SearchServiceCount
from UserHub.tasks import get_instagram_task
from UserHub.scraping import check_account
from UserHub.helper import max_engagement_rate_posts,most_watches_reels, max_reels_engagement_rate, hashtag_count,user_tags_count, calculate_engagement_rate, sorted_date,str_to_int, most_comments_posts,most_likes_posts,most_comments_reels,most_likes_reels
import json
import ast
from UserHub.storages import read_json_from_s3
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

logger = logging.getLogger(__name__)

# @vary_on_cookie
# @cache_page(60*60*60)
def sample_analyze_user(request):
    username = "davidbeckham"
    user_account = User.objects.get(username="deryacortuk")
    users = UserSearch.objects.filter(instagram_user=username,user=user_account).first()
    search_at = users.updated_at
    
    userfile = f"deryacortuk-{username}-posts"
    user = read_json_from_s3(userfile)
    profile = user["profile"]
    followers = str_to_int(user["profile"]["followers"])
    
    datafile =  f"de-{username}-detail-posts"
    user_data = read_json_from_s3(datafile)
    posts_len = len(user_data)
    new_data = sorted_date(username,"deryacortuk")
  
    post_chart_len = len(new_data)
    for data in new_data:        
        if "engagement_rate" in data:
            data["post_rate"] = round((data["engagement_rate"]/followers) * 100,2)    
            
            
        
    max_posts= max_engagement_rate_posts(username,"deryacortuk")
    for data in max_posts:
        data["post_rate"] = round((data["engagement_rate"]/followers) * 100,2)
        
    max_reels = max_reels_engagement_rate(username,"deryacortuk")
    for data in max_reels:
        data["reel_rate"] = round((data["engagement_rate"]/followers) * 100,2)
        
    hashtags = hashtag_count(username,"deryacortuk")
    captions = user_tags_count(username,"deryacortuk")
    
    total_engagement_rate = calculate_engagement_rate(username,"deryacortuk")
    
    most_likes = most_likes_posts(username,"deryacortuk")
    watches_reels = most_watches_reels(username,"deryacortuk")
    most_comments = most_comments_posts(username,"deryacortuk")
    reels_watch = most_likes_reels(username,"deryacortuk")
    reels_comments = most_comments_reels(username,"deryacortuk")
    return render(request, "userhub/analyse.html",{"profile":profile,"data":new_data, "updated_at":search_at,
        "max_posts":max_posts,"max_reels":max_reels,"hashtags":hashtags,"post_chart_len":post_chart_len,
        "captions":captions,"engagement_rate":total_engagement_rate,"post_len":posts_len,
        "watches_reels":watches_reels,"reels_watch":reels_watch,"reels_comments":reels_comments,
        "most_comments":most_comments,"most_likes":most_likes})

def index(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username')
            search = SearchServiceCount.objects.filter(user=request.user).first()
            if search.quantity > 0:
                check_username = check_account(username)
                if check_username == "This Account is Private":
                    message = f"{username} account is private!"                    
                    return render(request,"userhub/discovery.html",{"message":message})
                if check_username == "Sorry, this page isn't available":
                    message = f"{username} page isn't available! "
                    return render(request,"userhub/discovery.html",{"message":message})
                user = request.user.username
                get_instagram_task.delay(username,user)                          
                message = f"When {username}'s Instagram profile analysis is completed, you will be notified by e-mail and the analysis result will be on your analysis list page. Thank you for your patient. "
             
        
                return render(request,"userhub/discovery.html",{"message":message})
            
            message = "Please upgrade your account"
            return render(request,"pricing.html",{"message":message}) 
        
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
            
            send_mail(subject, message,"info@xlookin.com",[to_email], fail_silently=False)
            
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

@vary_on_cookie
@cache_page(60*60*60)
def about(request):   
    return render(request, "about.html")

from django.core.mail import send_mail

def contact(request):
   
    if request.method == "POST":
        message_name = request.POST['contact']
        message_email = request.POST['email']
        message_content = request.POST['message']
        
        email_send = EmailMessage(
        subject=message_name, 
        body=message_content, 
        from_email="info@xlookin.com",  
        to=['info@xlookin.com'],
        reply_to=[message_email])     
        
        email_send.send()
        message = "Thank you for contacting us. We have received your request and our team will get in touch with you shortly to assist you with your query."
        return render(request, 'contact.html',{'message':message})
        
    return render(request,'contact.html')

@vary_on_cookie
@cache_page(60*60*60)
def policy_privacy(request):    
    return render(request,"policy.html")

@vary_on_cookie
@cache_page(60*60*60)
def faq(request):
    return render(request,"faq.html")

def handler_not_found(request,exception):    
    return render(request,'404.html')

def handler_server_error(request):    
    return render(request,'500.html')


    
def handler_400(request,exception):    
    return render(request, '400.html')

def handler403(request,exception):    
    return render(request, '403.html')