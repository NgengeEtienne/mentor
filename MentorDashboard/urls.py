# urls.py
from django.urls import path
from . import views

name='MentorDashboard'
# app_name = 'mentor'
urlpatterns = [
    path('login/', views.mentor_login, name='mentor_login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.dashboard_overview, name='dashboard'),

    path('menu/', views.meal_plan_list, name='meal_plan_list'),
    path('menu/<int:id>/', views.meal_plan_detail, name='meal_plan_detail'),

    # path('profile', views.profile, name='profile'),
    path('deliver/', views.delivery_address_list, name='delivery_address_list'),
    path('delivery-address/add/', views.delivery_address_create, name='delivery_address_create'),
    path('delivery-address/edit/<int:id>/', views.delivery_address_edit, name='delivery_address_edit'),
    path('delivery-address/delete/<int:id>/', views.delivery_address_delete, name='delivery_address_delete'),
    # Add URLs for MealDelivery and Notification similarly
    # path('meal-deliveries/', views.meal_delivery_list, name='meal_delivery_list'),
    # path('meal-deliveries/list/', views.meal_delivered, name='meal_delivered'),
    path('meal-deliveries/<int:id>/edit/', views.meal_delivery_edit, name='meal_delivery_edit'),
    path('meal-deliveries/assign-address/post/', views.assign_meal_post, name='assign_address_ajax'),
    path('meal-deliveries/assign-address/<str:date>/', views.assign_meal, name='assign_address'),
    path('meal-deliveries/edit-assigned-address/<int:id>/<str:date>/', views.edit_assign_meal, name='edit_assign_address'),
    # path('meal-deliveries/asign-meal/', views.edit_assign_meal_without_date, name='edit_assign_meal_without_date'),
    path('meals_ordered/', views.meal_ordered, name='meal_ordered'),
    path('orders/today/', views.orders_today, name='orders_today'),  # List of all orders
    path('orders/', views.orders_list, name='orders_list'),  # List of all orders
    # path('orders/<int:id>/', views.order_detail, name='order_detail'),  # Order detail by ID



###############################################!MENTORS ONLY!################################################


    # Optional branch_id for meal plan list and detail
    path('menu/branches/', views.meal_plan_list, name='meal_plan_branches'),
    path('menu/<int:branch_id>/', views.meal_plan_list, name='meal_plan_list_by_branch'),
    path('menu/<int:branch_id>/<int:id>/', views.meal_plan_detail, name='meal_plan_detail_by_branch'),

    # Optional branch_id for delivery address list and actions
    path('delivery-addresses/', views.delivery_address_list, name='delivery_address_branches'),
    path('deliver/<int:branch_id>/', views.delivery_address_list, name='delivery_address_list_by_branch'),
    path('delivery-address/add/<int:branch_id>/', views.delivery_address_create, name='delivery_address_create_by_branch'),
    path('delivery-address/edit/<int:branch_id>/<int:id>/', views.delivery_address_edit, name='delivery_address_edit_by_branch'),
    path('delivery-address/delete/<int:branch_id>/<int:id>/', views.delivery_address_delete, name='delivery_address_delete_by_branch'),

    # Meal delivery URLs with optional branch_id
    path('meal-deliveries/branches/', views.meal_delivery_branches, name='meal_delivery_branches'),
    path('meal-deliveries/<int:branch_id>/<int:id>/edit/', views.meal_delivery_edit, name='meal_delivery_edit_by_branch'),
    path('meal-deliveries/assign-address/<int:branch_id>/post/', views.assign_meal_post, name='assign_address_ajax_by_branch'),
    path('meal-deliveries/assign-address/<int:branch_id>/<str:date>/', views.assign_meal, name='assign_address_by_branch'),
    path('meal-deliveries/edit-assigned-address/<int:branch_id>/<int:id>/<str:date>/', views.edit_assign_meal, name='edit_assign_address_by_branch'),
    path('meal-deliveries/status/<int:id>/', views.meal_delivery_edit, name='edit_status'),

    # Meals ordered with optional branch_id
    path('meals_ordered/branches/', views.meal_ordered_branches, name='meal_ordered_branches'),
    path('meals_ordered/<int:branch_id>/', views.meal_ordered, name='meal_ordered_by_branch'),

    # Orders list and today's orders with optional branch_id
    path('orders/today/branches/', views.orders_today, name='orders_today_branches'),
    path('orders/today/<int:branch_id>/', views.orders_today, name='orders_today_by_branch'),

    path('orders/branches/', views.orders_list, name='orders_branches'),
    path('orders/<int:branch_id>/', views.orders_list, name='orders_list_by_branch'),

     path('set-branch/<int:branch_id>/', views.set_branch_session, name='set_branch_session'),
]



