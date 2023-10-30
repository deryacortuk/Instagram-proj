from .scraping import get_instagram
from .helper import max_engagement_rate_posts,most_watches_reels, max_reels_engagement_rate, hashtag_count,user_tags_count, calculate_engagement_rate, sorted_date,str_to_int, most_comments_posts,most_likes_posts,most_comments_reels,most_likes_reels
from django.http import JsonResponse
from .tasks import get_instagram_task
from .models import UserSearch, SearchServiceCount
import json
import ast
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from django.views import View
from pyppeteer import launch
import asyncio
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.decorators import login_required

@vary_on_cookie
@cache_page(60)
def user_search_list(request):
    search_list = UserSearch.objects.filter(user =request.user,status=True)
    
    if search_list.exists():
        return render(request,"userHub/search_list.html",{"search_list":search_list})
    return render(request,"userHub/search_list.html")


@vary_on_cookie
@cache_page(60*60*60)
def analyze_user(request, username):
    user = UserSearch.objects.filter(instagram_user=username).first()
    search_at = user.updated_at
    with open(f"userHubData/{username}-posts.json","r",encoding="utf-8") as file:
        user = json.load(file)
    profile = user["profile"]
    followers = str_to_int(user["profile"]["followers"])
    with open(f"userHubData/{username}-detail-posts.json", "r", encoding="utf-8")  as file:
        userdata = file.read()
        user_data = ast.literal_eval(userdata)
    
    new_data = list()
    for data in user_data:
        for d in data:
            new_data.append(d)
    posts_len = len(new_data)
    if len(new_data) > 20:
        new_data = new_data[:20]
    post_chart_len = len(new_data)
    for data in new_data:
        
        if "engagement_rate" in data:
            data["post_rate"] = round((data["engagement_rate"]/followers) * 100,2)
    for data in new_data:
        if data["post_rate"] < 0.1:
            data["post_rate"] = 0.2
        
    max_posts= max_engagement_rate_posts(username)
    for data in max_posts:
        data["post_rate"] = round((data["engagement_rate"]/followers) * 100,2)
        
    max_reels = max_reels_engagement_rate(username)
    for data in max_reels:
        data["reel_rate"] = round((data["engagement_rate"]/followers) * 100,2)
        
    hashtags = hashtag_count(username)
    captions = user_tags_count(username)
    total_engagement_rate = calculate_engagement_rate(username)
    
    most_likes = most_likes_posts(username)
    watches_reels = most_watches_reels(username)
    most_comments = most_comments_posts(username)
    reels_watch = most_likes_reels(username)
    reels_comments = most_comments_reels(username)
    return render(request, "userhub/analyse.html",{"profile":profile,"data":new_data, "updated_at":search_at,
        "max_posts":max_posts,"max_reels":max_reels,"hashtags":hashtags,"post_chart_len":post_chart_len,
        "captions":captions,"engagement_rate":total_engagement_rate,"post_len":posts_len,
        "watches_reels":watches_reels,"reels_watch":reels_watch,"reels_comments":reels_comments,
        "most_comments":most_comments,"most_likes":most_likes})
    
    
def json_data_download(request,username):
    
    with open(f"userHubData/{username}-posts.json", "r", encoding="utf-8") as file:
         user_profile = json.load(file)
    with open(f"userHubData/{username}-reels-data.json", "r", encoding="utf-8") as file2:        
        user_reels = json.load(file2) 
    with open(f"userHubData/{username}-detail-posts.json", "r", encoding="utf-8") as file3:
        
        userdata = file3.read()
        user_data = ast.literal_eval(userdata) 
    json_data = dict()
    json_data["user"] = user_profile
    json_data["reels"] = user_reels
    json_data["posts_detail"] = user_data
    
    
    response = HttpResponse(json.dumps(json_data, ensure_ascii=False), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{username}.json"'
    return response

    

class GeneratePdf(View):
    async def render_pdf(self, username):
        browser = await launch(headless=True)
        page = await browser.newPage()

        url = f"http://127.0.0.1:8000/q/{username}/"
        await page.setViewport({'width': 794, 'height': 1123})

        await page.goto(url)
        await page.waitForSelector('body')  

        
        pdf = await page.pdf(format='A3')

        await browser.close()

        return pdf

    def get(self, request, username,*args, **kwargs):
        
        url = f"http://127.0.0.1:8000/q/{username}/"  

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        
        pdf_content = loop.run_until_complete(self.render_pdf(url))

        
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{username}.pdf"'

        return response
