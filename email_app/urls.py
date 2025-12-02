from django.urls import path
from . import views

urlpatterns = [
    path('send-mail/', views.send_mail_view, name='send_mail'),
    path('email-message/', views.email_message_view, name='email_message'),
]
