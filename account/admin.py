from django.contrib import admin

from .models import CustomUser, Company, Branch

admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(Branch)