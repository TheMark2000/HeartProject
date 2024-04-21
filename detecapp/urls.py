# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('' ,views.home, name='home'),
    path('prediction_form', views.predict, name='prediction_form'),
    path('registration', views.registration, name='registration'),
    path('signin', views.signin, name='signin'),
    path('about', views.about, name='about'),
    path('signout', views.signout, name='signout'),
    path('bmi_calculator', views.bmi_calculator, name='bmi_calculator'),
    path('bmi_results', views.bmi_results, name='bmi_results'),
]

