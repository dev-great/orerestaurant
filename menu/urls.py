from django.urls import path
from .views import *

app_name = 'menu'
urlpatterns = [
    path('image/', MenuItemImageView.as_view(), name='menu-image'),
    path('create/', MenuItemCreateView.as_view(), name='menu-create'),
    path('edit/<uuid:pk>/', MenuItemEditView.as_view(), name='menu-edit'),
    path('<uuid:pk>/', GetMenuItemByIDView.as_view(),
         name='menu-by-id'),
    path('', GetAllMenuItemsView.as_view(),
         name='all-menu'),
    path('discounted/', GetDiscountedMenuItemsView.as_view(),
         name='discounted-menu-items'),
    path('drinks/', GetDrinksMenuItemsView.as_view(), name='drinks-menu-items'),
]
