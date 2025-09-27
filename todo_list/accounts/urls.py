from django.urls import path
from .views import register_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html", redirect_authenticated_user=True), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="login"), name="logout"), # redirect after POST
]