from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Task

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Task


class UserAdmin(BaseUserAdmin):
    # Add the 'role' field to the admin panel
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),  # Adds a section for role
    )
    
    # Columns to display in the user list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    
    # Filters on the right sidebar in admin
    list_filter = ('role', 'is_staff', 'is_superuser')

# Register the User model with your custom UserAdmin
admin.site.register(User, UserAdmin)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Columns to display in task list
    list_display = ('title', 'assigned_to', 'status', 'due_date', 'worked_hours')
    
    # Filters for status, due date, and assigned user
    list_filter = ('status', 'due_date', 'assigned_to')
    
    # Search bar for title, description, or assigned user's username
    search_fields = ('title', 'description', 'assigned_to__username')

