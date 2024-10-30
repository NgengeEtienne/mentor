from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Company, Branch

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Customizing the add_fieldsets to include username and password fields
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'username',  # Added username
                'password1', 
                'password2', 
                'is_staff', 
                'is_active', 
                'is_superuser',  # Added superuser permission
                'company', 
                'branch', 
                'role',
            ),
        }),
    )

    # Customize fieldsets for change user form, including username and excluding date_joined

    list_display = UserAdmin.list_display
    search_fields = UserAdmin.search_fields
    ordering = UserAdmin.ordering
    filter_horizontal = UserAdmin.filter_horizontal
    list_filter = UserAdmin.list_filter

    # Override the save_model method to ensure password is hashed
    def save_model(self, request, obj, form, change):
        if 'password1' in form.cleaned_data and form.cleaned_data['password1']:
            obj.set_password(form.cleaned_data['password1'])
        super().save_model(request, obj, form, change)

# Register your models with the admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Company)
admin.site.register(Branch)
