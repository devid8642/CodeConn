from django.contrib import admin

from .models import ProjectIdea


@admin.register(ProjectIdea)
class ProjectIdeasAdmin(admin.ModelAdmin):
    list_display = ('idea', 'level', 'start_date')
    list_display_links = ('idea',)
    list_filter = ('level', 'start_date')
    search_fields = ('idea', 'level', 'start_date')
    ordering = ('-id',)
