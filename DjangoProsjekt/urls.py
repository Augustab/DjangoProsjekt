"""DjangoProsjekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
import main.views as v
import signup.views as v2


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', v.home, name="home"),
    path('signup/', v2.signup, name="signup"),
    path('regnskap/', v.regnskap, name="regnskap"),
    path('slett_sum/', v.slett_sum, name="slett_sum"),
    path('legg_til_sum/', v.legg_til_sum, name="legg_til_sum"),
    path('', v.redirect, name="redirect"),
    path('', include("django.contrib.auth.urls")),
]
