from django import forms
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class WeatherForm(forms.Form):
    city = forms.CharField(
        required=False,
        max_length=100,
        label="Город",
        widget=forms.TextInput(attrs={'placeholder': 'Введите название города'})
    )
    latitude = forms.FloatField(
        required=False,
        label="Широта",
        widget=forms.NumberInput(attrs={'placeholder': 'Широта'})
    )
    longitude = forms.FloatField(
        required=False,
        label="Долгота",
        widget=forms.NumberInput(attrs={'placeholder': 'Долгота'})
    )

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")

        if not city and (latitude is None or longitude is None):
            raise forms.ValidationError("Введите либо город, либо широту и долготу.")
        if city and (latitude or longitude):
            raise forms.ValidationError("Введите только город или только координаты.")
        return cleaned_data


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
