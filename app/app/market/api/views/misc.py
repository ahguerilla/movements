import json

from django.http import HttpResponse
from postman.models import Message
from django.contrib.auth.decorators import login_required


@login_required
def get_unreadCount(request, rtype):
    try:
        count = Message.objects.inbox_unread_count(request.user)
    except:
        return HttpResponse( json.dumps(0), mimetype="application/"+rtype)
    return HttpResponse( json.dumps(count), mimetype="application/"+rtype)
