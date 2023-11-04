from collections import Counter
import re
import json
import time
import ast
from datetime import datetime, timedelta
from UserHub.storages import read_json_from_s3



def find_hashtags(text):
    hashtags = re.findall(r'#(\w+)', text)
    return list(set(hashtags)) or []
    

def find_usernames(text):
    usernames = re.findall(r'@([a-zA-Z0-9._]+)', text)
    
    return list(set(usernames)) or []

def hashtag_count(username,user):
    filename = f"{user}-{username}-detail-posts"
    
    user_data = read_json_from_s3(filename)
    all_hashtags = []
    for post in user_data:
        hashtags = post.get('hashtags', [])
        all_hashtags.extend(hashtags)
    hashtags_count = Counter(all_hashtags)
    top_10_hashtags = hashtags_count.most_common(10)
    hashtag_list = {}
    for hashtag, count in top_10_hashtags:
        hashtag_list[hashtag] = count
    return hashtag_list

def user_tags_count(username,user):
    
    filename = f"{user}-{username}-detail-posts"
    user_data = read_json_from_s3(filename)
    all_tags = []
    for post in user_data:
        if "tags" in post:
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



def calculate_engagement_rate(username,user):
    
    profilefile = f"{user}-{username}-posts"
    user_profile = read_json_from_s3(profilefile)
    user_followers = user_profile["profile"]["followers"]
    
    followers = str_to_int(user_followers)
    
    
    datafile =  f"{user}-{username}-detail-posts"
    user_data = read_json_from_s3(datafile)
    
    result = 0
    
    for data in user_data:
        
        if "engagement_rate" in data:         
            result += data["engagement_rate"]
   
    engagement_rate = round(((result/len(user_data))/followers) * 100,2)
    return engagement_rate
        


        
def max_engagement_rate_posts(username,user):
    
    datafile =  f"{user}-{username}-detail-posts"
    user_data = read_json_from_s3(datafile)
 
    sorted_data = sorted(user_data, key=lambda x: x.get("engagement_rate", 0), reverse=True)
    if len(sorted_data) > 10:
         return sorted_data[:10]
    
    return sorted_data
    


def max_reels_engagement_rate(username,user):
    
    datafile =  f"{user}-{username}-reels-data"
    user_data = read_json_from_s3(datafile)
    
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
        
def sorted_date(username,user):
    
    datafile =  f"{user}-{username}-detail-posts"
    user_data = read_json_from_s3(datafile)

    sorted_user_data = sorted([(parse_date(date_string["time"]), date_string) for date_string in user_data if "time" in date_string], key=lambda x: x[0],reverse=True)
    sorted_user_data = [item[1] for item in sorted_user_data if item[0] is not None]   
                  
  
    if len(sorted_user_data) > 20:
        return sorted_user_data[:20]
    return sorted_user_data
    

def most_likes_posts(username,user):
  
    datafile =  f"{user}-{username}-detail-posts"
    user_data = read_json_from_s3(datafile)
    
    sorted_data = sorted(user_data, key=lambda x: x.get("likes", 0), reverse=True)
    if len(sorted_data) > 9:
        return sorted_data[:9]
    
    return sorted_data


def most_comments_posts(username,user):
  
    datafile =  f"{user}-{username}-detail-posts"
    user_data = read_json_from_s3(datafile)
    
    
    sorted_data = sorted(user_data, key=lambda x: x.get("comments", 0), reverse=True)
    if len(sorted_data) > 9:
        return sorted_data[:9]
    
    return sorted_data

def most_comments_reels(username,user):
   
    datafile =  f"{user}-{username}-reels-data"
    user_data = read_json_from_s3(datafile)
        
    sorted_data = sorted(user_data, key=lambda x: x.get("comments", 0), reverse=True)
    if len(sorted_data) > 9:
        return sorted_data[:9]
    
    return sorted_data
def most_likes_reels(username,user):
    
    datafile =  f"{user}-{username}-reels-data"
    user_data = read_json_from_s3(datafile)
        
    sorted_data = sorted(user_data, key=lambda x: x.get("likes", 0), reverse=True)
    if len(sorted_data) > 9:
        return sorted_data[:9]
    
    return sorted_data
def most_watches_reels(username,user):
  
    datafile =  f"{user}-{username}-reels-data"
    user_data = read_json_from_s3(datafile)
        
    sorted_data = sorted(user_data, key=lambda x: x.get("watch", 0), reverse=True)
    if len(sorted_data) > 9:
        return sorted_data[:9]
    
    return sorted_data

