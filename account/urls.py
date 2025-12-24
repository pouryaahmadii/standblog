from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.user_register, name='register'),
    path('edit', views.user_edit, name='edit'),

]