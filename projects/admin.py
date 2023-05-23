from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'is_approved', 'date_created')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_editable = ('is_approved',)
    list_filter = ('is_approved', )
    ordering = ('-id', '-date_created')
