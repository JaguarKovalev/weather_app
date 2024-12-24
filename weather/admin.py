from django.contrib import admin
from .models import WeatherRequest, UserProfile

# Регистрация модели WeatherRequest
@admin.register(WeatherRequest)
class WeatherRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'latitude', 'longitude', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('city', 'latitude', 'longitude', 'user__username')

# Регистрация модели UserProfile (если используется)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
