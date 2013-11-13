from app.market.forms import commentForm
import app.market as market
import app.users as users
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext
import json
from app.api.utils import *


obj_types={
    'offer':market.models.Offer,
    'request':market.models.Request,
    'resource':market.models.Resource
}


def saveComment(form, owner):
    import datetime
    if form.instance.pk == None:
        form.cleaned_data['owner'] = owner
        form.cleaned_data['pub_date'] = datetime.datetime.now()
    obj = form.save()
    obj.save()
    return obj


def addComment(request, obj_type, obj_id, rtype):
    obj = get_object_or_404(obj_types[obj_type].objects.only('comments'),pk=obj_id)
    form = commentForm(request.POST)
    if form.is_valid():
        saveComment(form,request.user)
        return HttpResponse(json.dumps({ 'success' : True}), mimetype="application"+rtype)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)), mimetype="application"+rtype)


def getlenComments(request, obj_type, obj_id, rtype):
    pass


def getCommentIds(request, obj_type, obj_id, rtype):
    pass


def getCommentIdsRange(request, obj_type, obj_id,st_date, end_date, rtype):
    pass


def getComment(request, obj_id, rtype):
    obj = get_object_or_404(market.models.Comment,pk=obj_id)
    return HttpResponse(value(rtype,[obj]), mimetype="application"+rtype)


def getComments(request,obj_type,obj_id,count,rtype):
    objs = obj_types[obj_type].filter(id=obj_id).only('comments')


def editComment(request,obj_id, rtype):
    obj = get_object_or_404(market.models.Comment,pk=obj_id)
    form = commentForm(request.POST, instance=obj)
    if form.is_valid():
        saveComment(form,request.user)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)), mimetype="application/"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),mimetype="application"+rtype)



def deleteComment(request, obj_id, rtype):
    pass
