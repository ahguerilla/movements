from app.market.forms import CommentForm
import app.market as market
import json
from app.market.api.utils import *
from django.contrib.auth.decorators import login_required
from tasks.celerytasks import create_comment_notification


@login_required
def add_comment(request, obj_id, rtype):
    m_obj = get_object_or_404(market.models.MarketItem.objects.only('pk'), pk=obj_id)
    form = CommentForm(request.POST)
    if form.is_valid():        
        obj = form.save(request.user, m_obj)
        create_comment_notification.delay(m_obj, obj, request.user.username)
        return HttpResponse(json.dumps({'success': True, 'obj': obj.getdict()}),
                            mimetype="application"+rtype)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)),
                            mimetype="application"+rtype)


@login_required
def get_comments(request, obj_id, count, rtype):
    obj = get_object_or_404(market.models.MarketItem, pk=obj_id)
    comments = obj.comments.filter(deleted=False).filter(published=True).order_by('-pub_date').all()[:count]
    retval = HttpResponse(json.dumps([c.getdict() for c in comments]),
                          mimetype="application" + rtype)
    return retval
    

@login_required
def edit_comment(request, obj_id, rtype):
    obj = get_object_or_404(market.models.Comment, pk=obj_id, deleted=False)
    form = CommentForm(request.POST, instance=obj)
    if form.is_valid():
        form.save(request.user, obj)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)), mimetype="application/"+rtype)
    return HttpResponse(json.dumps({'success': True}),
                        mimetype="application"+rtype)


@login_required
@check_perms_and_get(market.models.Comment)
def delete_comment(request, obj_id, rtype):
    obj = request.obj
    obj.deleted = True
    obj.item.commentcount -= 1
    obj.item.save()
    obj.save_base()
    return HttpResponse(json.dumps({'success': True}),
                        mimetype="application"+rtype)
