import json

from app.market.api.utils import *
import app.users as users
from django.http import HttpResponse
from postman.models import Message
from django.contrib.auth.decorators import login_required


#@login_required
def get_issues(request,rtype):
    issues = users.models.Issues.objects.all()
    return HttpResponse( value(rtype,issues), mimetype="application/"+rtype)


#@login_required
def get_countries(request,rtype):
    cntrs = users.models.Countries.objects.all()
    return HttpResponse( value(rtype,cntrs), mimetype="application/"+rtype)


@login_required
def get_nationalities(request,rtype):
    ntnlts = users.models.Nationality.objects.all()
    return HttpResponse( value(rtype,ntnlts), mimetype="application/"+rtype)


#@login_required
def get_skills(request,rtype):
    sklls = users.models.Skills.objects.all()
    return HttpResponse( value(rtype,sklls), mimetype="application/"+rtype)


@login_required
def get_unreadCount(request,rtype):
    try:
        count=Message.objects.inbox_unread_count(request.user)
    except:
        return HttpResponse( json.dumps(0), mimetype="application/"+rtype)
    return HttpResponse( json.dumps(count), mimetype="application/"+rtype)
