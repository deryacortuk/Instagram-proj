from celery import shared_task
from celery.utils.log import get_task_logger
from .scraping import process_url, scrape_website
import logging
import asyncio
from django.core.mail import  get_connection, EmailMessage
from UserHub.models import UserSearch, SearchServiceCount
from django.contrib.auth.models import User
from UserHub.celery_beat_scraping import beat_login_instagram,beat_process_url,beat_scrape_website
import time


logger = logging.getLogger("Celery")
    
logger = get_task_logger(__name__)    

@shared_task
def mail_created(username,user):
    profile = User.objects.get(username=user) 
    conn = get_connection(backend='django.core.mail.backends.smtp.EmailBackend')
    subject = f"Completion of {username}'s Instagram Profile Analysis"
    message = f' Dear {user.first_name}, \n \n' \
              f"The analysis of {username}'s Instagram profile has been completed successfully and you can view it on your list page.  \n \n Thank you so much for your patient!   \n \n Best regards, \n XLookin"
    
    mail_send = EmailMessage(subject=subject,body=message,
     from_email='info@xlookin.com',    
        to=[profile.email]) 
    
    return mail_send.send()

@shared_task
def get_instagram_task(username,users):
    user = User.objects.get(username=users)
    UserSearch.objects.create(user=user,instagram_user=username) 
    loop = asyncio.get_event_loop()        
    result = loop.run_until_complete(scrape_website(username,user))  
    if result == "Data was uploaded!":
    
        res = process_url(username,user)     
        if res == "Process was completed successfully":
        
        
            search = UserSearch.objects.filter(user=user,instagram_user=username).first()
            search.status = True        
            servicesearch = SearchServiceCount.objects.get(user=user)
            servicesearch.quantity -= 1
            search.status_code = servicesearch.status
            servicesearch.save()
            search.save()
        
            return mail_created(username,user)
        else:
            return "Something wrong"
    else:
        return "Something wrong"
    
@shared_task
def celery_cron_tasks():    
    instagramuser = UserSearch.objects.all().filter(status=False)
    
    if len(instagramuser) > 0:
        
        resl = beat_login_instagram()
        
        if resl[0] == "success":
            
            driver = resl[1]
            
            for info in instagramuser:
                
                loop = asyncio.get_event_loop()        
                result = loop.run_until_complete(beat_scrape_website(info.instagram_user,driver,info.user))          
                if result == "Data was uploaded!":
                    res = beat_process_url(info.instagram_user,info.user)     
                
                    if res == "Process was completed successfully":
        
        
                        search = UserSearch.objects.filter(user=info.user,instagram_user=info.instagram_user).first()
                        search.status = True        
                        servicesearch = SearchServiceCount.objects.get(user=info.user)
                        servicesearch.quantity -= 1
                        search.status_code = servicesearch.status
                        servicesearch.save()
                        search.save()
        
                        mail_created(info.instagram_user,info.user)
                        
                    
            driver.quit()
            return "Process was successfull!"
        else:
            resl[1].quit()
            time.sleep(60)
            return celery_cron_tasks()
    return "OK"

