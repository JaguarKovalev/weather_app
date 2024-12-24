from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import WeatherForm
from .models import WeatherRequest
import requests

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm

from django.shortcuts import render
from .forms import WeatherForm
import requests

from django.http import JsonResponse

def forecast(request):
    form = WeatherForm()
    labels = []
    temperatures = []

    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data.get('city')
            latitude = form.cleaned_data.get('latitude')
            longitude = form.cleaned_data.get('longitude')
            api_key = "482adb12c18eaf2ee9c6a2dac8e6c7b3"

            if city:
                url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ru"
            else:
                url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric&lang=ru"

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for item in data['list'][:10]:  # Ограничиваем до 10 точек
                    labels.append(item['dt_txt'])
                    temperatures.append(item['main']['temp'])

    return render(request, 'weather/forecast.html', {
        'form': form,
        'labels': labels,
        'temperatures': temperatures,
    })




# Главная страница
def home(request):
    return render(request, 'weather/home.html')

# Поиск погоды по городу
from django.core.cache import cache

# Закешированное представление
from .models import WeatherRequest

def weather_by_city(request):
    form = WeatherForm()
    weather_data = None

    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data.get('city')
            cache_key = f"weather_city_{city.lower()}"  # Ключ кэша
            weather_data = cache.get(cache_key)  # Проверяем кэш

            if not weather_data:  # Если данных в кэше нет
                api_key = "482adb12c18eaf2ee9c6a2dac8e6c7b3"
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    weather_data = {
                        'city': data.get('name', 'Неизвестно'),
                        'temperature': data['main']['temp'],
                        'description': data['weather'][0]['description'],
                        'icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
                    }
                    cache.set(cache_key, weather_data, 600)  # Сохраняем в кэш на 10 минут
                else:
                    weather_data = {'error': 'Не удалось получить данные. Проверьте ввод.'}

            # Сохраняем запрос в базу данных
            if request.user.is_authenticated:
                WeatherRequest.objects.create(
                    user=request.user,
                    city=city,
                    result=weather_data
                )

    return render(request, 'weather/by_city.html', {'form': form, 'weather_data': weather_data})



# не закешированное представление
def weather_by_coordinates(request):
    form = WeatherForm()
    weather_data = None

    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data.get('latitude')
            longitude = form.cleaned_data.get('longitude')
            api_key = "482adb12c18eaf2ee9c6a2dac8e6c7b3"
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric&lang=ru"

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': data.get('name', f"Координаты: {latitude}, {longitude}"),
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
                }
                # Сохраняем запрос в базу данных, если пользователь авторизован
                if request.user.is_authenticated:
                    WeatherRequest.objects.create(
                        user=request.user,
                        latitude=latitude,
                        longitude=longitude,
                        result=weather_data
                    )
            else:
                weather_data = {'error': 'Не удалось получить данные. Проверьте ввод.'}

    return render(request, 'weather/by_coordinates.html', {'form': form, 'weather_data': weather_data})


# История запросов
@login_required
def history(request):
    requests = WeatherRequest.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'weather/history.html', {'requests': requests})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически логиним пользователя после регистрации
            return redirect('home')  # Редирект на главную страницу
    else:
        form = UserRegisterForm()
    return render(request, 'weather/register.html', {'form': form})
