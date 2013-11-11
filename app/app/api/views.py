from app.market.forms import newofferForm
import app.market as market
import app.users as users
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_validation_errors(form):
    return { 'success' : False,
             'errors' : [(k, form.error_class.as_text(v)) for k, v in form.errors.items()] }


def value(atype,objs,**kwargs):
    return serializers.serialize(atype,objs,**kwargs)


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


def newOffer(request):
    form = newofferForm(request.POST)
    if form.is_valid():
        form.cleaned_data['ip_address'] = get_client_ip(request)
        form.cleaned_data['owner'] = request.user
        obj = form.save()
        obj.save()
        form.save_m2m()
    else:
        return HttpResponse(get_validation_errors(form))
    return HttpResponse('ok')


def editOffer(request,obj_id):
    obj = get_object_or_404(market.models.Offer,pk=obj_id)
    return render_to_response('market/offer.html',
	                          {'offer':value('json',[obj])},
	                          context_instance=RequestContext(request))
