from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'address', 'mobile_number']
    search_fields = ['name', 'email']


admin.site.register(Profile, ProfileAdmin)
