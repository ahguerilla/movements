import json

from app.api.utils import *
import app.market as market
from app.market.forms import newofferForm
import app.users as users
from django.core import serializers
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext


def getSCRFToken(request,rtype):
    c={}
    c.update(csrf(request))
    return HttpResponse( json.dumps({'csrfmiddlewaretoken': c['csrf_token'].decode()}), mimetype="application/"+rtype)


def getIssues(request,rtype):
    issues = users.models.Issues.objects.all()
    return HttpResponse( value(rtype,issues), mimetype="application/"+rtype)


def getCountries(request,rtype):
    cntrs = users.models.Countries.objects.all()
    return HttpResponse( value(rtype,cntrs), mimetype="application/"+rtype)


def getNationalities(request,rtype):
    ntnlts = users.models.Nationality.objects.all()
    return HttpResponse( value(rtype,ntnlts), mimetype="application/"+rtype)


def getSkills(request,rtype):
    sklls = users.models.Skills.objects.all()
    return HttpResponse( value(rtype,sklls), mimetype="application/"+rtype)

