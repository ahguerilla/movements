from app.market.forms import commentForm
import app.market as market
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
from app.market.api.utils import *
from django.contrib.auth.decorators import login_required
from celerytasks import createCommentNotification


def saveComment(form, owner,item):
    import datetime
    if form.is_valid() and form.instance.pk == None:
        form.cleaned_data['owner'] = owner
        form.cleaned_data['item'] = item
        form.cleaned_data['pub_date'] = datetime.datetime.now()
    obj = form.save()
    obj.save()
    obj.save_base()
    return obj


@login_required
def addComment(request, obj_id, rtype):
    m_obj = get_object_or_404(market.models.MarketItem.objects.only('pk'),pk=obj_id)
    form = commentForm(request.POST)
    if form.is_valid():
        obj = saveComment(form,request.user,m_obj)
        createCommentNotification.delay(m_obj,request.user.username)
        return HttpResponse(json.dumps({ 'success' : True, 'obj': obj.getdict() }), mimetype="application"+rtype)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)), mimetype="application"+rtype)


@login_required
def getCommentCount(request, obj_id, rtype):
    obj = get_object_or_404(market.models.MarketItem.objects.only('commentcount'),pk=obj_id)
    return HttpResponse(json.dumps(obj.commentcount), mimetype="application"+rtype)


@login_required
def getCommentIds(request, obj_id, rtype):
    pass


@login_required
def getCommentIdsRange(request, obj_id,st_date, end_date, rtype):
    pass


@login_required
def getComment(request, obj_id, rtype):
    obj = get_object_or_404(market.models.Comment, pk=obj_id, deleted=False)
    return HttpResponse(value(rtype,[obj]), mimetype="application"+rtype)


@login_required
def getComments(request,obj_id,count,rtype):
    obj = get_object_or_404(market.models.MarketItem, pk=obj_id)
    comments = obj.comments.filter(deleted=False).filter(published=True).order_by('-pub_date').all()[:count]
    return HttpResponse(json.dumps([c.getdict() for c in comments]),
                        mimetype="application"+rtype)


@login_required
def editComment(request,obj_id, rtype):
    obj = get_object_or_404(market.models.Comment, pk=obj_id, deleted=False)
    form = commentForm(request.POST, instance=obj)
    if form.is_valid():
        saveComment(form,request.user,None)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)), mimetype="application/"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),mimetype="application"+rtype)



@login_required
@check_perms_and_get(market.models.Comment)
def deleteComment(request, obj_id, rtype):
    obj = request.obj
    obj.deleted = True
    obj.item.commentcount -= 1
    obj.item.save()
    obj.save_base()
    return HttpResponse(json.dumps({ 'success' : True}),mimetype="application"+rtype)
