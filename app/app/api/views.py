from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers

import app.users as users


def value(atype,objs):
	return serializers.serialize(atype,objs)


def issues(request,rtype):
	issues = users.models.Issues.objects.all()
	return HttpResponse( value(rtype,issues), mimetype="application/"+rtype)


def countries(request,rtype):
	cntrs = users.models.Countries.objects.all()
	return HttpResponse( value(rtype,cntrs), mimetype="application/"+rtype)


def nationalities(request,rtype):
	ntnlts = users.models.Nationality.objects.all()
	return HttpResponse( value(rtype,ntnlts), mimetype="application/"+rtype)


def skills(request,rtype):
	sklls = users.models.Skills.objects.all()
	return HttpResponse( value(rtype,sklls), mimetype="application/"+rtype)


def newoffer(request):
	issues = request.POST.getlist('issues[]')
	countries = request.POST.getlist('countries[]')
	skills = request.POST.getlist('skills[]')
	title = request.POST.get('title')
	exp_date = request.POST.get('exp_date')
	details = request.POST.get('details')