from django.urls import path
from UserHub.views import   analyze_user, user_search_list,json_data_download, posts_convert_to_csv, reels_data_to_csv
app_name = "userhub"

urlpatterns = [
   
    path("",user_search_list,name="search_list"),
    path("<username>/", analyze_user, name="analysis"),
    path("download/<username>/",json_data_download, name="download"),
    path('convert/<username>/', posts_convert_to_csv, name='posts_convert_to_csv'),
    path('reels/<username>/', reels_data_to_csv, name='reels_convert_to_csv'),
    #path('generate-pdf/<username>/', generate_pdf, name='generate_pdf'),
    
    
]
