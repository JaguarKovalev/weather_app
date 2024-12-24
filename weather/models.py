from django.contrib.auth.models import User
from django.db import models

class WeatherRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weather_requests")
    city = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    result = models.JSONField()  # Хранит ответ от API

    def __str__(self):
        if self.city:
            return f"Запрос: {self.city} ({self.timestamp})"
        return f"Запрос: {self.latitude}, {self.longitude} ({self.timestamp})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    preferences = models.JSONField(default=dict)  # Например, предпочтительный язык или единицы измерения

    def __str__(self):
        return f"Профиль {self.user.username}"
