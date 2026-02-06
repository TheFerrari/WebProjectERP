from django.contrib import admin
from .models import BranchDirectory

@admin.register(BranchDirectory)
class BranchDirectoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'timezone')
