from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler500

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Account.urls",namespace="account")),
    path("q/",include("UserHub.urls", namespace="userhub")),     
     path("order/", include("Order.urls",namespace="order")),
      path("payment/", include("Payment.urls",namespace="payment")),
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 


handler404 = 'Account.views.handler_not_found'
handler500 = 'Account.views.handler_server_error'
handler400 = 'Account.views.handler_400'
handler403 = 'Account.views.handler403'