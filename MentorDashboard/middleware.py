from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from account.models import Branch,CustomUser,Company

class BranchCompanyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            if request.user.is_authenticated:
                # Retrieve all branches and companies related to the user
                request.branch = request.user.branch.all()  # queryset of branches
                request.company = request.user.company.all()  # queryset of companies
                # print(request.branch, request.company)

                # If you need only the first branch or company, use .first()
                request.branch = request.user.branch.all().first()  # First branch, if needed
                request.company = request.user.company.all().first()  # First company, if needed
                # print(request.branch, request.company)

                # user = CustomUser.objects.get(email="et@gmail.com")  # Replace with an actual user email
                # print(user.branch.all())  # Should return queryset of branches if populated
                # print(user.company.all())  # Should return queryset of companies if populated

            else:
                # Handle unauthenticated users by setting to empty querysets
                request.branches = Branch.objects.none()  # Empty queryset for branches
                request.companies = Company.objects.none()  # Empty queryset for companies
                request.branch = None
                request.company = None
                print("unauth")



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
