from django.urls import path
from .views import   analyze_user, user_search_list,json_data_download
app_name = "userhub"

urlpatterns = [
   
    path("",user_search_list,name="search_list"),
    path("<username>/", analyze_user, name="analysis"),
    path("download/<username>/",json_data_download, name="download"),
    #path('generate-pdf/<username>/', generate_pdf, name='generate_pdf'),
    
    
]
