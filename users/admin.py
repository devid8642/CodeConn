from django.contrib import admin

from .models import User
from .models import ProjectsDate


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'username', 'is_active', 'is_staff', 'date_joined'
    )
    list_display_links = ('id', 'email', 'username')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-id', '-date_joined')
    search_fields = ('username', 'email')


@admin.register(ProjectsDate)
class ProjectsDateAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date')
    list_display_links = ('start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('start_date', 'end_date')
    # list_editable = ('start_date', 'end_date')
