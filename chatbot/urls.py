# 3) Made urls.py in chatbot app

from django.urls import path
from . import views
urlpatterns = [
    path('',views.chatbot, name='chatbot'),
    
     # 13) login and register
    
    path('login',views.login, name='login'),
    path('register',views.register, name='register'),
    path('logout',views.logout, name='logout')
]