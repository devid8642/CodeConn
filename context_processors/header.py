from projects.models import Comment, Project


def notifications(request):
    comments = Comment.objects.filter(
        read=False,
        project__author=request.user.id,
    ).order_by('-id')
    projects = Project.objects.filter(
        author=request.user.id
    )
    complaints = []
    notifications = 0 + comments.count()

    for project in projects:
        if project.complaints_notifications:
            complaints.append(project)
            notifications += 1

    return {
        'comments_notification': comments,
        'notifications_count': notifications,
        'complaints': complaints,
    }
