from django.urls import path
from . import views

urlpatterns=[
    path('', views.Chat.as_view(), name='chat'),

]