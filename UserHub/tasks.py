from celery import shared_task
from celery.utils.log import get_task_logger
from .scraping import process_url, scrape_website
import logging
import asyncio
from .helper import sorted_date
from django.core.mail import  get_connection, EmailMessage
from UserHub.models import UserSearch, SearchServiceCount
from django.contrib.auth.models import User



logger = logging.getLogger("Celery")
    
logger = get_task_logger(__name__)    

@shared_task
def mail_created(username,user):
    profile = User.objects.get(username=user) 
    conn = get_connection(backend='django.core.mail.backends.smtp.EmailBackend')
    subject = f'Instagram user: {username}'
    message = f'Dear {user.first_name}, \n\n' \
              f'{username} Instagram profile analyzed successfully. Thanks so much for your patient!   \n \n Best regards, \n \n SellorBuy'
    
    mail_send = EmailMessage(subject=subject,body=message,
     from_email='sellorbuy@sellorbuy.shop',    
        to=[profile.email]) 
    
    return mail_send.send()

@shared_task
def get_instagram_task(username,users):
    user = User.objects.get(username=users)
    UserSearch.objects.create(user=user,instagram_user=username) 
    loop = asyncio.get_event_loop()        
    result = loop.run_until_complete(scrape_website(username))
    if result == "This Account is Private":
        return "Account is private!"
    
    res = process_url(username)    
    if res == "Process was completed successfully":
        sorted_date(username)
        
        search = UserSearch.objects.filter(user=user,instagram_user=username).first()
        search.status = True
        search.save()
        servicesearch = SearchServiceCount.objects.get(user=user)
        servicesearch.quantity -= 1
        servicesearch.save()
        
        return mail_created(username,user)
    else:
        return "Something wrong"


