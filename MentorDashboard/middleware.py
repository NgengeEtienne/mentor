from django.utils.deprecation import MiddlewareMixin
from AdminDashboard.models import Branch, Company

class BranchCompanyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
           
            request.branch = Branch.objects.get(id=request.user.branch.id)
            request.company = Company.objects.get(id=request.user.branch.company_id)

            # request.company= Company.objects.get(id=1)
            # request.branch = Branch.objects.get(id=1)
        else:
            request.branch = Branch.objects.get(id=request.user.branch.id)
            request.company = Company.objects.get(id=request.user.branch.company_id)