# resources.py
from import_export import resources
from.models import (
    Company,
    Branch,
    CustomUser,
    PasswordReset,
)

class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company
        fields = ('id', 'name', 'address_line_1', 'address_line_2', 'city','state', 'pin_code', 'latitude', 'longitude', 'date_created', 'date_updated')

class BranchResource(resources.ModelResource):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'company', 'address_line_1', 'address_line_2', 'city','state', 'pin_code', 'latitude', 'longitude', 'date_created', 'date_updated')
        export_order = ('id', 'name', 'company', 'address_line_1', 'address_line_2', 'city', 'tate', 'pin_code', 'latitude', 'longitude', 'date_created', 'date_updated')
		
class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'date_joined', 'company', 'branch', 'role')

class PasswordResetResource(resources.ModelResource):
    class Meta:
        model = PasswordReset
        fields = ('id', 'user', 'token', 'timestamp')