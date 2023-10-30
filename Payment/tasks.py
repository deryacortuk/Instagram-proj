from io import BytesIO
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from Order.models import Order
from celery.utils.log import get_task_logger
from Product.models import ServiceProduct
import logging

logger = logging.getLogger("Celery")

logger = get_task_logger(__name__)

@shared_task
def payment_completed(order_id):
    pass
    # order = Order.objects.get(id=order_id)
    # subject = f'SellorBuy Shop - EE Invoice no. {order.id}'
    # message = f'Dear {order.user.first_name},\n\n Thank you for shopping at SellorBuy. We will be very glad to assist you with any questions you have and give you all information about your order. \
    # \n If you have not received your package within 30 days from the shipping date, we shall be willing to refund your money or replace your items if any. A refund will be made in the same way as your payment was made. \
    # \n Thank you again for shopping at SellorBuy. \n\n Regards, \n\n SellorBuy '
    # email = EmailMessage(subject, message, 'sellorbuy@sellorbuy.shop',[order.email])
    # html = render_to_string('orders/pdf.html', {'order': order})
    # out = BytesIO()
    # stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0] +  '/css/pdf.css')]
    # weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
    # email.attach(f'order_{order.id}.pdf', out.getvalue(),'application/pdf')
    # email.send(fail_silently=False)