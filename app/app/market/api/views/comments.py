from app.market.forms import commentForm
import app.market as market
import app.users as users
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext
import json
from app.market.api.utils import *
from django.core.urlresolvers import reverse
import avatar


def createCommentDict(comment):
    adict={'fields':{}}       
    adict['fields']['pub_date'] = str(comment.pub_date)
    adict['fields']['contents'] = comment.contents
    adict['pk'] = comment.pk    
    adict['fields']['owner'] = comment.owner.id    
    adict['fields']['avatar'] = reverse('avatar_render_primary', args=[comment.owner.username,80])
    adict['fields']['username'] = comment.owner.username
    adict['fields']['profile_url'] = reverse('user_profile_for_user', args=[comment.owner.username])
    return adict
    
    
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
        obj = saveComment(form,request.user,obj)
        return HttpResponse(json.dumps({ 'success' : True, 'obj': createCommentDict(obj) }), mimetype="application"+rtype)
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
    return HttpResponse(json.dumps([createCommentDict(c) for c in comments]),
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
