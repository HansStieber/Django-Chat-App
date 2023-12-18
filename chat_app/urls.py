"""
URL configuration for chat_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from chat.views import index, login_view, register_view, user_logout, select_chat, create_chat

urlpatterns = [
  path('admin/', admin.site.urls),
  path('chat/<int:chatId>/', index, name='chat_index'),
  path('create_chat/', create_chat, name='create_chat'),
  path('login/', login_view, name='login'),
  path('register/', register_view, name='register'),
  path('logout/', user_logout, name='logout'),
  path('select_chatpartner/', select_chat)
]
