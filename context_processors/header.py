from projects.models import Comment


def comments_notification(request):
    comments = Comment.objects.filter(
        read=False,
        project__author=request.user.id,
    ).order_by('-id')

    return {
        'comments_notification': comments,
        'comments_count': comments.count(),
    }
