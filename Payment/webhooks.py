import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Order.models import Order
from .tasks import payment_completed
from Product.models import ServiceProduct
from django.shortcuts import get_object_or_404
import os 
import dotenv
from UserHub.models import SearchServiceCount

env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
dotenv.load_dotenv(env_file)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    if event.type == "checkout.session.completed":
        session = event.data.object
        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            order.paid = True
            order.status = 'paid'                            
            
            order.stripe_id = session.payment_intent                           

            service_search = get_object_or_404(SearchServiceCount,user=order.user)
            for item in order.items.all():                
                
                product = get_object_or_404(ServiceProduct, id= item.product.id)                 
                              
                service_search.quantity += product.quantity
                service_search.status = product.name
                service_search.save()                               
                                                                                
            order.save() 
            payment_completed.delay(order.id)            
                
    return HttpResponse(status=200)