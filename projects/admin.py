from django.contrib import admin

from .models import Project, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'is_approved', 'created_at')
    list_display_links = ('id', 'title')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', )
    ordering = ('-id', '-created_at')
    search_fields = ('title', 'author__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'author', 'created_at', 'updated_at')
    list_filter = ('project__title', 'author__username')
    ordering = ('-created_at', '-id')
    search_fields = ('comment', 'author__username', 'project__title')