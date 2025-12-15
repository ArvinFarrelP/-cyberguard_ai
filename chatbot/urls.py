from django.urls import path
from .views import chatbot_view, chat_api, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('chat/', chatbot_view, name='chatbot'),
    path('api/chat/', chat_api, name='chat_api'),
]
