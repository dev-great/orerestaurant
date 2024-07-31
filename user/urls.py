from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/', AllUsersView.as_view(), name='all-users'),
    path('users/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),

]
