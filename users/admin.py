from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import ProjectsDate, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'is_active',
        'is_staff',
        'date_joined',
    )
    list_display_links = ('id', 'email', 'username')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-id', '-date_joined')
    search_fields = ('username', 'email')


admin.site.register(ProjectsDate, SingletonModelAdmin)
