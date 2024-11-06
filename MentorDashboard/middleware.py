from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from AdminDashboard.models import Branch, Company

class BranchCompanyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            if request.user.is_authenticated:
                # Retrieve all branches and companies related to the user
                request.branches = request.user.branch.all()  # queryset of branches
                request.companies = request.user.company.all()  # queryset of companies

                # If you need only the first branch or company, use .first()
                request.branch = request.user.branch.all().first()  # First branch, if needed
                request.company = request.user.company.all().first()  # First company, if needed
            else:
                # Handle unauthenticated users by setting to empty querysets
                request.branches = Branch.objects.none()  # Empty queryset for branches
                request.companies = Company.objects.none()  # Empty queryset for companies
                request.branch = None
                request.company = None

        except Exception as e:
            # Log any unexpected error and set to empty querysets
            request.branches = Branch.objects.none()
            request.companies = Company.objects.none()
            request.branch = None
            request.company = None
            print(f"An unexpected error occurred: {e}")

# middleware/restrict_admin.py

from django.shortcuts import redirect
from django.urls import reverse

class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is trying to access the admin panel
        if request.path.startswith(reverse('admin:index')):
            # If the user is authenticated but not a superuser, redirect them to the dashboard
            if request.user.is_authenticated and not request.user.is_superuser:
                return redirect('dashboard')  # Replace 'dashboard' with the name of your dashboard URL
        return self.get_response(request)
