from collections import Counter
import re
import json
import time
import ast
from datetime import datetime, timedelta


def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
        u"\U0001F1F2-\U0001F1F4"  
        u"\U0001F1E6-\U0001F1FF" 
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r'', text)

def find_hashtags(text):
    hashtags = re.findall(r'#(\w+)', text)
    return list(set(hashtags)) or []
    

def find_usernames(text):
    usernames = re.findall(r'@([a-zA-Z0-9._]+)', text)
    
    return list(set(usernames)) or []

def hashtag_count(username):
    with open(f"userHubData/{username}-detail-posts.json", "r", encoding="utf-8") as file:
        userdata = file.read()
        user_data = ast.literal_eval(userdata)
    new_data = list()
    for data in user_data:
        for d in data:
            new_data.append(d)
    all_hashtags = []
    for post in new_data:
        hashtags = post.get('hashtags', [])
        all_hashtags.extend(hashtags)
    hashtags_count = Counter(all_hashtags)
    top_10_hashtags = hashtags_count.most_common(10)
    hashtag_list = {}
    for hashtag, count in top_10_hashtags:
        hashtag_list[hashtag] = count
    return hashtag_list

def user_tags_count(username):
    with open(f"userHubData/{username}-detail-posts.json", "r", encoding="utf-8") as file:
        userdata = file.read()
        user_data = ast.literal_eval(userdata)
    new_data = list()
    for data in user_data:
        for d in data:
            new_data.append(d)
    all_tags = []
    for post in new_data:
        all_tags.extend(post["tags"])

    tag_counts = Counter(all_tags)
    top_tags = tag_counts.most_common(10)
    
    user_tag = {}
    for tag, count in top_tags:
        user_tag[tag] = count
    return user_tag

def str_to_int(data):
    number = data.replace(',', '').replace('.', '')
    if number[-1] == 'M':
        return int(float(number[:-1]) * 1000000)  
    elif number[-1] == 'K':
        return int(float(number[:-1]) * 1000) 
    else:
        return int(number)



def calculate_engagement_rate(username):
    with open(f"userHubData/{username}-posts.json", "r", encoding="utf-8") as file:
        user_profile = json.load(file)
    user_followers = user_profile["profile"]["followers"]
    
    followers = str_to_int(user_followers)
    
    with open(f"userHubData/{username}-detail-posts.json", "r", encoding="utf-8") as file:
        userdata = file.read()
        user_data = ast.literal_eval(userdata)
    new_data = list()
    
    for data in user_data:
        for d in data:
            new_data.append(d)
    result = 0
    
    for data in new_data:
        
        if "engagement_rate" in data:         
            result += data["engagement_rate"]
   
    engagement_rate = round(((result/len(new_data))/followers) * 100,2)
    return engagement_rate
        
    
# def reels_engagement_rate(username):
#     with open(f"userHubData/{username}-posts.json", "r", encoding="utf-8") as file:
#         user_profile = json.load(file)
#     user_followers = user_profile["profile"]["followers"]
    
#     followers = str_to_int(user_followers)
    
#     with open(f"userHubData/{username}-reels-data.json","r", encoding="utf-8") as file:
#         reelsdata = file.read()         
#         user_data = ast.literal_eval(reelsdata)
#     result = 0
#     for data in user_data:
#         if "engagement_rate" in data:
#             result += data["engagement_rate"]
    
#     engagement_rate = round(((result/len(user_data))/followers) * 100,2)
#     return engagement_rate
        
def max_engagement_rate_posts(username):
    with open(f"userHubData/{username}-detail-posts.json", "r", encoding="utf-8") as file:
        userdata = file.read()
        user_data = ast.literal_eval(userdata)
    new_data = list()
    for data in user_data:
        for d in data:
            new_data.append(d)
    sorted_data = sorted(new_data, key=lambda x: x["engagement_rate"], reverse=True)
    if len(sorted_data) > 10:
        return sorted_data[:10]
    
    return sorted_data
    


def max_reels_engagement_rate(username):
    with open(f"userHubData/{username}-reels-data.json","r", encoding="utf-8") as file:
        reelsdata = file.read()         
        user_data = ast.literal_eval(reelsdata)
    
    sorted_data = sorted(user_data, key=lambda x: x.get("engagement_rate", 0), reverse=True)
    if len(sorted_data) > 10:
        return sorted_data[:10]
    return sorted_data



def parse_date(date_string):
    current_date = datetime.now()
    if date_string == None:
        return None
    if "MINUTES AGO" in date_string:
        minutes_ago = int(re.search(r'\d+', date_string).group())
        return current_date - timedelta(minutes=minutes_ago)
    elif "HOURS AGO" in date_string:
        hours_ago = int(re.search(r'\d+', date_string).group())
        return current_date - timedelta(hours=hours_ago)
    elif "HOUR AGO" in date_string:
        hours_ago = int(re.search(r'\d+', date_string).group())
        return current_date - timedelta(hours=hours_ago)
    elif "DAYS AGO" in date_string:
        days_ago = int(re.search(r'\d+', date_string).group())
        return current_date - timedelta(days=days_ago)
    elif "DAY AGO" in date_string:
        days_ago = int(re.search(r'\d+', date_string).group())
        return current_date - timedelta(days=days_ago)
    elif "," in date_string:
        try:
           
            formatted_date = datetime.strptime(date_string, "%B %d, %Y")
            return formatted_date
        except ValueError:
            return None
    else:
        try:
            
            formatted_date = datetime.strptime(date_string, "%B %d")
            if formatted_date.month > current_date.month or (formatted_date.month == current_date.month and formatted_date.day > current_date.day):
               
                return formatted_date.replace(year=current_date.year - 1)
            else:
                return formatted_date.replace(year=current_date.year)
        except ValueError:
            return None
        
def sorted_date(username):
    with open(f"userHubData/{username}-detail-posts.json", "r", encoding="utf-8")  as file:
        userdata = file.read()
        user_data = ast.literal_eval(userdata)       

    sorted_user_data = sorted([(parse_date(date_string["time"]), date_string) for date_string in user_data], key=lambda x: x[0],reverse=True)
    sorted_user_data = [item[1] for item in sorted_user_data if item[0] is not None]   
                  
  
    with open(f"userHubData/{username}-detail-posts.json","w",encoding="utf-8") as file:
            json_data = json.dumps(sorted_user_data,indent=4,ensure_ascii=False)                
            file.write(json_data + ",")
    

def most_likes_posts(username):
    with open(f"userHubData/{username}-detail-posts.json", "r", encoding="utf-8") as file:
        userdata = file.read()
        user_data = ast.literal_eval(userdata)
    new_data = list()
    for data in user_data:
        for d in data:
            new_data.append(d)
    sorted_data = sorted(new_data, key=lambda x: x.get("likes", 0), reverse=True)
    if len(sorted_data) > 9:
        return sorted_data[:9]
    
    return sorted_data


def most_comments_posts(username):
    with open(f"userHubData/{username}-detail-posts.json", "r", encoding="utf-8") as file:
        userdata = file.read()
        user_data = ast.literal_eval(userdata)
    new_data = list()
    for data in user_data:
        for d in data:
            new_data.append(d)
    sorted_data = sorted(new_data, key=lambda x: x.get("comments", 0), reverse=True)
    if len(sorted_data) > 9:
        return sorted_data[:9]
    
    return sorted_data

def most_comments_reels(username):
    with open(f"userHubData/{username}-reels-data.json", "r", encoding="utf-8") as file:
        userdata = file.read()
        user_data = ast.literal_eval(userdata)
        
    sorted_data = sorted(user_data, key=lambda x: x.get("comments", 0), reverse=True)
    if len(sorted_data) > 9:
        return sorted_data[:9]
    
    return sorted_data
def most_likes_reels(username):
    with open(f"userHubData/{username}-reels-data.json", "r", encoding="utf-8") as file:
        userdata = file.read()
        user_data = ast.literal_eval(userdata)
        
    sorted_data = sorted(user_data, key=lambda x: x.get("likes", 0), reverse=True)
    if len(sorted_data) > 9:
        return sorted_data[:9]
    
    return sorted_data
def most_watches_reels(username):
    with open(f"userHubData/{username}-reels-data.json", "r", encoding="utf-8") as file:
        userdata = file.read()
        user_data = ast.literal_eval(userdata)
        
    sorted_data = sorted(user_data, key=lambda x: x.get("watch", 0), reverse=True)
    if len(sorted_data) > 9:
        return sorted_data[:9]
    
    return sorted_data

