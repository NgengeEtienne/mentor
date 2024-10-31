# urls.py
from django.urls import path
from . import views
from .views import (
    delivery_address_list, delivery_address_create, 
    delivery_address_edit, delivery_address_delete
)

name='MentorDashboard'
urlpatterns = [
    path('login/', views.mentor_login, name='mentor_login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.dashboard_overview, name='dashboard'),

    path('mealplan', views.meal_plan_list, name='meal_plan_list'),
    path('mealplan/<int:id>/', views.meal_plan_detail, name='meal_plan_detail'),

    # path('profile', views.profile, name='profile'),
    path('deliver', delivery_address_list, name='delivery_address_list'),
    path('delivery-address/add/', delivery_address_create, name='delivery_address_create'),
    path('delivery-address/edit/<int:id>/', delivery_address_edit, name='delivery_address_edit'),
    path('delivery-address/delete/<int:id>/', delivery_address_delete, name='delivery_address_delete'),
    # Add URLs for MealDelivery and Notification similarly
    # path('meal-deliveries/', views.meal_delivery_list, name='meal_delivery_list'),
    # path('meal-deliveries/list/', views.meal_delivered, name='meal_delivered'),
    path('meal-deliveries/<int:id>/edit/', views.meal_delivery_edit, name='meal_delivery_edit'),
    path('meal-deliveries/assign-address/post/', views.assign_meal_post, name='assign_address_ajax'),
    path('meal-deliveries/assign-address/<str:date>/', views.assign_meal, name='assign_address'),
    path('meal-deliveries/edit-assigned-address/<int:id>/<str:date>/', views.edit_assign_meal, name='edit_assign_address'),
    # path('meal-deliveries/asign-meal/', views.edit_assign_meal_without_date, name='edit_assign_meal_without_date'),
    path('meals_ordered', views.meal_ordered, name='meal_ordered'),
    path('orders/', views.orders_list, name='orders_list'),  # List of all orders
    # path('orders/<int:id>/', views.order_detail, name='order_detail'),  # Order detail by ID
]


