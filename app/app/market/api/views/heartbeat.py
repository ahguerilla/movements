import json

from django.http import HttpResponse
from postman.models import Message
from app.market.models import Notification
from django.contrib.auth.decorators import login_required


@login_required
def get_counts(request):
    count_notifications = Notification.objects.filter(user=request.user.id, item__deleted=False, seen=False).count()
    count_messages = Message.objects.inbox_unread_count(request.user)
    counts = {
        'messages': count_messages,
        'notifications': count_notifications
    }
    return HttpResponse(json.dumps(counts), mimetype="application/json")
