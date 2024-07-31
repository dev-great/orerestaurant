from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('profile/', UserProfileView.as_view()),
    path('users', AllUsersView.as_view(), name='all_users'),
    path('users/<uuid:pk>/', UserDetailView.as_view(), name='user_by_id'),

]
