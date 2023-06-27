from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import User, ProjectIdea
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


@admin.register(ProjectIdea)
class ProjectIdeasAdmin(admin.ModelAdmin):
    list_display = ('idea', 'level', 'start_date')
    list_display_links = ('idea',)
    list_filter = ('level', 'start_date')
    search_fields = ('idea', 'level', 'start_date')
    ordering = ('-id',)


admin.site.register(ProjectsDate, SingletonModelAdmin)
