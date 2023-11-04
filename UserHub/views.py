
from UserHub.helper import max_engagement_rate_posts,most_watches_reels, max_reels_engagement_rate, hashtag_count,user_tags_count, calculate_engagement_rate, sorted_date,str_to_int, most_comments_posts,most_likes_posts,most_comments_reels,most_likes_reels
from django.http import JsonResponse
from UserHub.tasks import get_instagram_task
from UserHub.models import UserSearch, SearchServiceCount
import json
import ast
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from django.views import View
import asyncio
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import HttpResponse
from UserHub.storages import read_json_from_s3
from django.contrib.auth.models import User

# @vary_on_cookie
# @cache_page(60)
def user_search_list(request):
    search_list = UserSearch.objects.filter(user =request.user,status=True)
    
    if search_list.exists():
        return render(request,"userHub/search_list.html",{"search_list":search_list})
    return render(request,"userHub/search_list.html")


# @vary_on_cookie
# @cache_page(60*60*60)
def analyze_user(request, username):
    user_account = User.objects.get(username=request.user)
    users = UserSearch.objects.filter(instagram_user=username,user=request.user).first()
    search_at = users.updated_at
    
    userfile = f"{user_account}-{username}-posts"
    user = read_json_from_s3(userfile)
    profile = user["profile"]
    followers = str_to_int(user["profile"]["followers"])
    
    datafile =  f"{user_account}-{username}-detail-posts"
    user_data = read_json_from_s3(datafile)
    posts_len = len(user_data)
    new_data = sorted_date(username,user_account)
  
    post_chart_len = len(new_data)
    for data in new_data:        
        if "engagement_rate" in data:
            data["post_rate"] = round((data["engagement_rate"]/followers) * 100,2)    
            
            
        
    max_posts= max_engagement_rate_posts(username,user_account)
    for data in max_posts:
        data["post_rate"] = round((data["engagement_rate"]/followers) * 100,2)
        
    max_reels = max_reels_engagement_rate(username,user_account)
    for data in max_reels:
        data["reel_rate"] = round((data["engagement_rate"]/followers) * 100,2)
        
    hashtags = hashtag_count(username,user_account)
    captions = user_tags_count(username,user_account)
    
    total_engagement_rate = calculate_engagement_rate(username,user_account)
    
    most_likes = most_likes_posts(username,user_account)
    watches_reels = most_watches_reels(username,user_account)
    most_comments = most_comments_posts(username,user_account)
    reels_watch = most_likes_reels(username,user_account)
    reels_comments = most_comments_reels(username,user_account)
    return render(request, "userhub/analyse.html",{"profile":profile,"data":new_data, "updated_at":search_at,
        "max_posts":max_posts,"max_reels":max_reels,"hashtags":hashtags,"post_chart_len":post_chart_len,
        "captions":captions,"engagement_rate":total_engagement_rate,"post_len":posts_len,
        "watches_reels":watches_reels,"reels_watch":reels_watch,"reels_comments":reels_comments,
        "most_comments":most_comments,"most_likes":most_likes})
    
    
def json_data_download(request,username):
    
    user = User.objects.get(username=request.user)
    userfile = f"{user}-{username}-posts"
    user_profile = read_json_from_s3(userfile)
    
    reelfile = f"{user}-{username}-reels-data"
    user_reels = read_json_from_s3(reelfile)
    
    
    userdata = f"{user}-{username}-detail-posts"
    user_data = read_json_from_s3(userdata)
    
    json_data = dict()
    json_data["user"] = user_profile
    json_data["reels"] = user_reels
    json_data["posts_detail"] = user_data
    
    
    response = HttpResponse(json.dumps(json_data, ensure_ascii=False), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{username}.json"'
    return response

def posts_convert_to_csv(request,username):
    
    if username == "davidbeckham":
        userdata = f"deryacortuk-{username}-detail-posts"
        user_data = read_json_from_s3(userdata)        
    
        new_data = user_data
    
        df = pd.DataFrame(new_data)        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data-posts-detail.csv"'
        df.to_csv(path_or_buf=response, index=False, encoding='utf-8')
        return response
    
    user = User.objects.get(username=request.user)        
    
        
    userdata = f"{user}-{username}-detail-posts"
    user_data = read_json_from_s3(userdata)        
    
    new_data = user_data
    
    df = pd.DataFrame(new_data)        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data-posts-detail.csv"'
    df.to_csv(path_or_buf=response, index=False, encoding='utf-8')
    return response
    

def reels_data_to_csv(request,username):
    if username == "davidbeckham":
        userdata = f"de-{username}-reels-data"
        user_reels = read_json_from_s3(userdata)
        df = pd.DataFrame(user_reels)        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data-reels.csv"'
        df.to_csv(path_or_buf=response, index=False, encoding='utf-8')
        return response
    user = User.objects.get(username = request.user)   
       
    userdata = f"{user}-{username}-reels-data"
    user_reels = read_json_from_s3(userdata)
    df = pd.DataFrame(user_reels)        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data-reels.csv"'
    df.to_csv(path_or_buf=response, index=False, encoding='utf-8')
    return response

