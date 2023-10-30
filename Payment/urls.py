from django.urls import path
from . import views
from .webhooks import stripe_webhook
app_name = 'payment'

urlpatterns = [
 path('process/', views.payment_process, name='process'),
 path('done/', views.payment_done, name='done'),
 path('canceled/', views.payment_canceled, name='canceled'),
 path("webhook/",stripe_webhook, name="stripe_webhook"),
]