import json

from app.market.forms import CommentForm
import app.market as market
from app.market.api.utils import *
from django.contrib.auth.decorators import login_required
from app.celerytasks import create_comment_notification
from django.views.decorators.http import require_http_methods
from app.market.models import Comment, MarketItemCollaborators


@login_required
def add_comment(request, obj_id, rtype):
    m_obj = get_object_or_404(market.models.MarketItem.objects.only('pk'), pk=obj_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        obj = form.save(request.user, m_obj)
        create_comment_notification.delay(m_obj, obj, request.user.username)

        item = market.models.MarketItem.objects.get(id=obj_id)
        if item:
            market_collaborator = MarketItemCollaborators()
            market_collaborator.market_item_id = obj_id
            market_collaborator.collaborator_id = obj.owner_id
            market_collaborator.interaction_type = "Comment"
            market_collaborator.save()

            # Recalc number of collaborators and store in market item.
            item.collaboratorcount = MarketItemCollaborators.objects.filter(market_item_id=obj_id).values(
                "collaborator_id").distinct().count()
            item.save()

        return HttpResponse(json.dumps({'success': True, 'obj': obj.getdict()}),
                            mimetype="application"+rtype)
    else:
        return HttpResponse(json.dumps(get_validation_errors(form)),
                            mimetype="application"+rtype)


def get_comments(request, obj_id, count, rtype):
    obj = get_object_or_404(market.models.MarketItem, pk=obj_id)
    comments = obj.comments.filter(deleted=False).filter(published=True).order_by('-pub_date').all()[:count]
    retval = HttpResponse(json.dumps([c.getdict() for c in comments]),
                          mimetype="application" + rtype)
    return retval


@login_required
@require_http_methods(["POST"])
def delete_comment(request):
    is_success = False
    obj_id = request.POST.get("commentID", 0)
    try:
        comment = Comment.objects.get(pk=obj_id)
    except Comment.DoesNotExist:
        comment = None

    if comment:
        if request.user.id == comment.owner.id:
            is_success = True
            comment.deleted = True
            comment.item.commentcount -= 1
            comment.item.save()
            comment.save_base()

    return HttpResponse(json.dumps({'success': is_success}), mimetype="application/json")
