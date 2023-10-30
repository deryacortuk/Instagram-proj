from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from django.urls import reverse
import logging
from django.contrib.auth.decorators import login_required
from Product.models import ServiceProduct
from UserHub.models import UserSearch, SearchServiceCount

logger = logging.getLogger(__name__)


def order_creates(request):    
    
    if request.method == "POST":        
        name = request.POST.get("title")
        print(name)
        product = get_object_or_404(ServiceProduct,name=name)
        user = request.user
        order = Order.objects.create(user=user)
                          
        OrderItem.objects.create(order=order,product=product,price=product.price)        
       
        request.session['order_id'] = order.id                
            
                
        return redirect(reverse("payment:process"))
    