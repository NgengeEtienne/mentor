from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from AdminDashboard.models import Branch, Company

class BranchCompanyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            if request.user.is_authenticated:
                request.branch = Branch.objects.get(id=request.user.branch.id)
                request.company = Company.objects.get(id=request.user.branch.company_id)
            else:
                # Handle unauthenticated users
                # You can either set defaults or raise an error
                request.branch = None  # Set to a default branch
                request.company = None  # Set to a default company

        except Branch.DoesNotExist:
            # Handle case where branch does not exist
            request.branch = None  # or some default branch
            # Optionally log the error or raise an exception
            print(f"Branch not found for user {request.user.id}")

        except Company.DoesNotExist:
            # Handle case where company does not exist
            request.company = None  # or some default company
            # Optionally log the error or raise an exception
            print(f"Company not found for branch {request.user.branch.id}")

        except Exception as e:
            # Handle any other exception
            request.branch = None
            request.company = None
            # Log the error message
            print(f"An unexpected error occurred: {e}")
