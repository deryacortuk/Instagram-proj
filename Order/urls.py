from django.urls import path
from Order.views import order_creates

app_name = "order"

urlpatterns = [
   path("",order_creates, name="create_order"),
]
