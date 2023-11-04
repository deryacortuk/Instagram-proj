from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from Order.models import Order
from celery.utils.log import get_task_logger
from django.core.mail import  get_connection, EmailMessage
import logging

logger = logging.getLogger("Celery")

logger = get_task_logger(__name__)

@shared_task
def payment_completed(order_id):
    conn = get_connection(backend='django.core.mail.backends.smtp.EmailBackend')
    order = Order.objects.get(id=order_id)
    subject = f'XLookin - EE Invoice no. {order.id}'
    message = f"Dear {order.order_user.first_name},\n\n Thank you for upgrading to our premium membership program! Your payment has been processed successfully and your account has been upgraded to premium. \
    \n We appreciate your continued support and hope that you find value in the additional features that come with your premium membership. \
    \n Please don't hesitate to reach out to us if you have any questions or concerns.  \n\n Best Regards, \n XLookin "
    mail_send = EmailMessage(subject=subject,body=message, from_email='info@xlookin.com', to=[order.order_user.email]) 
    
    return mail_send.send()