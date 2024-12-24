from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('by-city/', views.weather_by_city, name='weather_by_city'),
    path('by-coordinates/', views.weather_by_coordinates, name='weather_by_coordinates'),
    path('history/', views.history, name='history'),
]



urlpatterns += [
    path('login/', auth_views.LoginView.as_view(template_name='weather/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
urlpatterns += [
    path('register/', views.register, name='register'),
]

urlpatterns += [
    path('forecast/', views.forecast, name='forecast'),
]
