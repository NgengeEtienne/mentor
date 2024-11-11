from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Company, Branch
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from.models import (
    Company,
    Branch,
    CustomUser,
    PasswordReset,
)
from.resources import (
    CompanyResource,
    BranchResource,
    CustomUserResource,
    PasswordResetResource,
)

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'username',
                'password1', 
                'password2', 
                'is_staff', 
                'is_active', 
                'is_superuser',
                'company', 
                'branch', 
                'role',
                'date_joined',  # Include date_joined in add_fieldsets
            ),
        }),
    )

    fieldsets = (
        (None, {
            'fields': (
                'username', 
                'email', 
                                'password', 
                # 'password2', 
                'is_staff', 
                'is_active', 
                'is_superuser', 
                'company', 
                'branch', 
                'role',
                'date_joined',  # Include date_joined in fieldsets
            ),
        }),
        ('Permissions', {
            'fields': ('user_permissions',),
        }),
        ('Important dates', {
            'fields': ('last_login',),
        }),
    )

    # The rest of your CustomUserAdmin remains unchanged...


    # Customize display fields in the user list
    list_display = ('email', 'username', 'get_companies', 'get_branches', 'role', 'is_staff', 'is_active')

    def get_companies(self, obj):
        return ", ".join([company.name for company in obj.company.all()])
    get_companies.short_description = 'Companies'

    def get_branches(self, obj):
        return ", ".join([branch.name for branch in obj.branch.all()])
    get_branches.short_description = 'Branches'
    search_fields = ('email', 'username', 'company__name', 'branch__name')  # Search by company and branch names
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ('is_staff', 'is_active', 'role', 'company', 'branch')

    # Override the save_model method to ensure password is hashed
    def save_model(self, request, obj, form, change):
        if 'password1' in form.cleaned_data and form.cleaned_data['password1']:
            obj.set_password(form.cleaned_data['password1'])
        super().save_model(request, obj, form, change)

# Register your models with the admin
admin.site.register(CustomUser, CustomUserAdmin)
@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    resource_class = CompanyResource

# Admin for Branch
@admin.register(Branch)
class BranchAdmin(ImportExportModelAdmin):
    resource_class = BranchResource


# class CustomUserAdmin(ImportExportModelAdmin):
#     resource_class = CustomUserResource