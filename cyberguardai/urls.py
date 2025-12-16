from django.contrib import admin
from django.urls import path, include
from chatbot.views import chatbot_view, chat_api, home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('chat/', chatbot_view, name='chatbot'),
    path('api/chat/', chat_api, name='chat_api'),
]

