from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('update-user/', views.updateUser, name='update-user'),
    path('profile/<int:pk>/', views.userprofile, name='profile')
]
