from app.market.forms import commentForm
import app.market as market
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
from app.market.api.utils import *
from django.contrib.auth.decorators import login_required
from tasks.celerytasks import create_comment_notification
from django.utils.cache import get_cache_key, get_cache
cache = get_cache('default')


def save_comment(form, owner,item):
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
def add_comment(request, obj_id, rtype):
    m_obj = get_object_or_404(market.models.MarketItem.objects.only('pk'), pk=obj_id)
    form = commentForm(request.POST)
    if form.is_valid():        
        obj = save_comment(form,  request.user ,m_obj)
        create_comment_notification.delay(m_obj, obj, request.user.username)
        cache.delete('allcomment-'+obj_id )        
        return HttpResponse(json.dumps({ 'success' : True, 'obj': obj.getdict() }),
                            mimetype="application"+rtype)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)),
                            mimetype="application"+rtype)


@login_required
def get_comment_count(request, obj_id, rtype):
    obj = get_object_or_404(market.models.MarketItem.objects.only('commentcount'),pk=obj_id)
    return HttpResponse(json.dumps(obj.commentcount),
                        mimetype="application"+rtype)


@login_required
def get_comment_ids(request, obj_id, rtype):
    pass


@login_required
def get_commentids_range(request, obj_id,st_date, end_date, rtype):
    pass


@login_required
def getComment(request, obj_id, rtype):
    retval = cache.get('comment-'+obj_id )
    if retval: 
        return retval         
    obj = get_object_or_404(market.models.Comment, pk=obj_id, deleted=False)
    retval = HttpResponse(value(rtype,[obj]),
                        mimetype="application"+rtype)
    cache.add('comment-'+obj_id,retval)
    return retval


@login_required
def get_comments(request,obj_id,count,rtype):
    retval = cache.get('allcomment-'+obj_id )
    if retval: 
        return retval             
    obj = get_object_or_404(market.models.MarketItem, pk=obj_id)
    comments = obj.comments.filter(deleted=False).filter(published=True).order_by('-pub_date').all()[:count]
    retval = HttpResponse(json.dumps([c.getdict() for c in comments]),
                        mimetype="application"+rtype)
    cache.add('allcomment-'+obj_id,retval)
    return retval    
    

@login_required
def edit_comment(request,obj_id, rtype):
    obj = get_object_or_404(market.models.Comment, pk=obj_id, deleted=False)
    form = commentForm(request.POST, instance=obj)
    if form.is_valid():
        comment = save_comment(form,request.user,None)
        cache.delete('allcomment-'+obj_id )
        cache.delete('comment-'+comment.id )
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)), mimetype="application/"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),
                        mimetype="application"+rtype)


@login_required
@check_perms_and_get(market.models.Comment)
def delete_comment(request, obj_id, rtype):
    obj = request.obj
    obj.deleted = True
    obj.item.commentcount -= 1
    obj.item.save()
    obj.save_base()
    cache.delete('allcomment-'+obj_id )    
    cache.delete('comment-'+obj.id )    
    return HttpResponse(json.dumps({ 'success' : True}),
                        mimetype="application"+rtype)
