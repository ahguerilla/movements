from app.market.forms import commentForm
import app.market as market
import app.users as users
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext
import json
from app.market.api.utils import *



def saveComment(form, owner,item):
    import datetime
    if form.instance.pk == None:
        form.cleaned_data['owner'] = owner
        form.cleaned_data['item'] = item
        form.cleaned_data['pub_date'] = datetime.datetime.now()
    obj = form.save()
    obj.save()
    return obj


def addComment(request, obj_id, rtype):
    obj = get_object_or_404(market.models.MarketItem.objects.only('pk'),pk=obj_id)
    form = commentForm(request.POST)
    if form.is_valid():
        saveComment(form,request.user,obj)
        return HttpResponse(json.dumps({ 'success' : True}), mimetype="application"+rtype)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)), mimetype="application"+rtype)


def getlenComments(request, obj_id, rtype):
    pass


def getCommentIds(request, obj_id, rtype):
    pass


def getCommentIdsRange(request, obj_id,st_date, end_date, rtype):
    pass


def getComment(request, obj_id, rtype):
    obj = get_object_or_404(market.models.Comment, pk=obj_id)
    return HttpResponse(value(rtype,[obj]), mimetype="application"+rtype)


def getComments(request,obj_id,count,rtype):
    obj = get_object_or_404(market.models.MarketItem, pk=obj_id)
    comments = obj.comments.filter(published=True).order_by('-pub_date').all()[:count]
    return HttpResponse(value(rtype,
                              comments,
                              indent=2,
                              #use_natural_keys=True
                              ),
                        mimetype="application"+rtype)


def editComment(request,obj_id, rtype):
    obj = get_object_or_404(market.models.Comment, pk=obj_id)
    form = commentForm(request.POST, instance=obj)
    if form.is_valid():
        saveComment(form,request.user,None)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)), mimetype="application/"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),mimetype="application"+rtype)



def deleteComment(request, obj_id, rtype):
    pass
