from django.urls import path
from . import views
from django.conf.urls import url
from .models import *
from django.conf import settings
from django.conf.urls.static import static

app_name='core'

urlpatterns = [
    path('input/', views.post_input, name='summary'),
    path('index/', views.index, name='index'),
    path('url-inp/', views.web_scrape, name='web_scrape'),   
] 