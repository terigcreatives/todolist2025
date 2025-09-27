from django.urls import path
from .views import welcome_view, contact_view

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('contact/', contact_view, name='contact_us'),
]