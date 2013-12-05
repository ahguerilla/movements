import json

from app.market.api.utils import *
import app.market as market
import app.users as users
from django.core import serializers
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext
from postman.models import Message
from django.contrib.auth.decorators import login_required


@login_required
def getSCRFToken(request,rtype):
    c={}
    c.update(csrf(request))
    return HttpResponse( json.dumps({'csrfmiddlewaretoken': c['csrf_token'].decode()}), mimetype="application/"+rtype)


@login_required
def getIssues(request,rtype):
    issues = users.models.Issues.objects.all()
    return HttpResponse( value(rtype,issues), mimetype="application/"+rtype)


@login_required
def getCountries(request,rtype):
    cntrs = users.models.Countries.objects.all()
    return HttpResponse( value(rtype,cntrs), mimetype="application/"+rtype)


@login_required
def getNationalities(request,rtype):
    ntnlts = users.models.Nationality.objects.all()
    return HttpResponse( value(rtype,ntnlts), mimetype="application/"+rtype)


@login_required
def getSkills(request,rtype):
    sklls = users.models.Skills.objects.all()
    return HttpResponse( value(rtype,sklls), mimetype="application/"+rtype)


@login_required
def getUnraedCount(request,rtype):
    try:
        count=Message.objects.inbox_unread_count(request.user)
    except:
        return HttpResponse( json.dumps(0), mimetype="application/"+rtype)
    return HttpResponse( json.dumps(count), mimetype="application/"+rtype)