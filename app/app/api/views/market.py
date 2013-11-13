from app.market.forms import newofferForm
import app.market as market
import app.users as users
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext
import json
from app.api.utils import *



def saveMarketItem(form, obj_type, owner):
    form.cleaned_data['item_type'] = obj_type
    form.cleaned_data['owner'] = owner
    obj = form.save()
    obj.save()
    form.save_m2m()


def addMarketItem(request, obj_type, rtype):
    form = newofferForm(request.POST)
    if form.is_valid():
        saveMarketItem(form, obj_type,request.user)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)), mimetype="application"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),mimetype="application"+rtype)


def getMarketItem(request,obj_id,rtype):
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'), pk=obj_id)
    return HttpResponse(
        value(rtype,
              [obj],
              use_natural_keys=True,
              fields=('issues','countries','skills','title','details', 'pub_date','exp_date', 'owner')
              ),
        mimetype="application/"+rtype)


def editMarketItem(request,obj_id,rtype):
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'),pk=obj_id)
    form = newofferForm(request.POST, instance=obj)
    if form.is_valid():
        saveMarketItem(form, obj.item_type, obj.owner)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)), mimetype="application/"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),mimetype="application"+rtype)


def deleteMarketItem(request,obj_id,rtype):
    pass
