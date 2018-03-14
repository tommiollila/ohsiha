from django.urls import path
from . import views

urlpatterns = [
    path('your-email/', views.your_email),
    path('register/', views.register, name='register'),
    path('base/', views.base),
    path('index/', views.index, name='index'),
    path('jquery/', views.jquery),
    path('profile/', views.profile, name='profile')
]
