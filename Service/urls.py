from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler500
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticViewSiteMap
from django.contrib.auth import views as auth_views 
from django.views.generic.base import TemplateView

sitemaps ={       
    'static':StaticViewSiteMap,        
    }

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Account.urls",namespace="account")),
    path("x/",include("UserHub.urls", namespace="userhub")),     
     path("order/", include("Order.urls",namespace="order")),
    path("payment/", include("Payment.urls",namespace="payment")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
     path('password-reset/',auth_views.PasswordResetView.as_view(
             template_name='account/password/password_reset.html',
             subject_template_name='account/password/password_reset_subject.txt',
             email_template_name='account/password/password_reset_email.html',),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(
             template_name='account/password/password_reset_mail_sent.html' ),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password/password_reset_confirmation.html'
         ),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password/password_reset_completed.html'
         ),name='password_reset_complete'),
    path("robots.txt",TemplateView.as_view(template_name="robot.txt", content_type="text/plain"),
    ),
    
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 


handler404 = 'Account.views.handler_not_found'
handler500 = 'Account.views.handler_server_error'
handler400 = 'Account.views.handler_400'
handler403 = 'Account.views.handler403'