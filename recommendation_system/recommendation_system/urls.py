"""recommendation_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recommender import views as recommender_views
from users import views as users_views
from django.contrib.auth import views as authentication_views

from users.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', recommender_views.index, name="index"),
    path('login/',
         authentication_views.LoginView.as_view(template_name='users/login.html', authentication_form=LoginForm),
         name='login'),
    path('logout/', authentication_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', users_views.register, name='register'),
    path('result/', recommender_views.result, name='result')
]
