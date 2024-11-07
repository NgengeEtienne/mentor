from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from account.models import Branch,CustomUser,Company

class BranchCompanyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            if request.user.is_authenticated:
                if request.user.role == 'BRANCH_MANAGER':
                    # Retrieve all branches related to the user
                    request.branch = request.user.branch.all()  # queryset of branches
                    request.company = request.user.company.all().first()  # First company, if 
                    print(request.branch)
                elif request.user.role == 'COMPANY_ADMIN':
                    # Retrieve all branches and companies related to the user
                    request.branch = Branch.objects.filter(company__in=request.user.company.all())
                    request.company = request.user.company.all()
                elif request.user.role == 'MENTOR':
                    request.branch = request.user.branch.all().first()
                    request.company = request.user.company.all().first()
                else:
                    # Retrieve the first branch and company related to the user
                    request.branch = None  # First branch, if needed
                    request.company = None
            else:
                # Handle unauthenticated users by setting to empty querysets
                request.branch = None
                request.company = None
                print("unauth")

        except Exception as e:
            # Log any unexpected error and set to empty querysets
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
