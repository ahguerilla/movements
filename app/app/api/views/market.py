from app.market.forms import item_forms,fileForm,saveMarketItem
import app.market as market
import app.users as users
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext
import json
from app.api.utils import *




def validate(request,obj_type):
    forms = [ form(request.POST,request.FILES) for form in item_forms[obj_type]['forms'] ]
    valid = [form.is_valid() for form in forms]
    if all(valid):
        return True,forms
    return False,forms


def save(request,forms,obj_type):
    objs=[]
    for form in forms:
        objs.append(item_forms[obj_type]['save'][form](form, obj_type, request.user,objs))


def addMarketItem(request, obj_type, rtype):
    form = item_forms[obj_type](request)
    if form.is_valid():
        save(request, forms, obj_type)
    else:
        return HttpResponse(json.dumps(get_validation_errors(forms)), mimetype="application"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),mimetype="application"+rtype)


def getMarketItem(request,obj_id,rtype):
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'), pk=obj_id)
    return HttpResponse(
        value(rtype,
              [obj],
              use_natural_keys=True,
              fields=('item_type','issues','countries','skills','title','details', 'pub_date','exp_date', 'owner', 'url','files')
              ),
        mimetype="application/"+rtype)


def editMarketItem(request,obj_id,rtype):
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'),pk=obj_id)
    form = item_forms[obj.item_type](request.POST, instance=obj)
    if form.is_valid():
        saveMarketItem(form, obj.item_type, obj.owner)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)), mimetype="application/"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),mimetype="application"+rtype)


def deleteMarketItem(request,obj_id,rtype):
    pass
