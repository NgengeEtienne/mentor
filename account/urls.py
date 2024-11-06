from django.urls import path, include
from .views import *
from. import views
from .views import csrf_token_view  # Import your view


name="account"
urlpatterns = [
    path('admin-login/', AdminLoginView.as_view(), name='login'),
    path('admin-logout/', AdminLogoutView.as_view(), name='logout'),

    path('reset-password/confirm_password/', CustomPasswordTokenVerificationView.as_view(), name='confirm_password'),  # confirm password
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('csrf-token/', csrf_token_view, name='csrf_token'),

    path('companies/', views.CompanyList.as_view()),
    path('companies/<int:pk>/', views.CompanyDetail.as_view()),
    path('branches/', views.BranchList.as_view()),
    path('branches/<int:pk>/', views.BranchDetail.as_view()),
    path('users/', views.CustomUserList.as_view()),
    path('users/<int:pk>/', views.CustomUserDetail.as_view()),
    path('companies/<int:company_id>/branches/', views.CompanyBranchList.as_view()),
    path('branches/<int:branch_id>/users/', views.BranchUsersList.as_view()),
]
