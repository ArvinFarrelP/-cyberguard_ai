# cyberguardai/urls.py - CORRECT VERSION
from django.contrib import admin
from django.urls import path
from chatbot.views import home_view, chat_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('api/chat/', chat_api, name='chat_api'),
]
