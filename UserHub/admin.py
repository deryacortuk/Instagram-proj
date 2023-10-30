from django.contrib import admin
from .models import UserProfile, UserSearch  , SearchServiceCount

admin.site.register(UserProfile)

@admin.register(UserSearch)
class SearchUserAdmin(admin.ModelAdmin):
    list_display = ["user","instagram_user","status","created_at","updated_at"]    
    list_filter = ["instagram_user","created_at"]
    class Meta:
        model = UserSearch
        
@admin.register(SearchServiceCount)
class SearchServiceAdmin(admin.ModelAdmin):
    list_display = ["user","created_at","updated_at","quantity"]
    list_filter = ["user","created_at"]
    class Meta:
        model = SearchServiceCount