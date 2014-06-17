import json
from datetime import datetime

from django.db.models import Q
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import login_required
import constance
import requests
from django.conf import settings
from django.utils.cache import get_cache

from app.market.api.utils import *
import app.market as market
from tasks.celerytasks import create_notification, update_notifications, mark_read_notifications, add_view
from users import create_query




cache = get_cache('default')
items_cache = get_cache('items')
user_items_cache = get_cache('user_items')


def get_market_json(objs, request=None):
    alist = []
    for obj in objs:
        alist.append(obj.getdict(request))
    return json.dumps(alist)


def return_item_list(obj, rtype, request=None):
    return HttpResponse(
        get_market_json(obj, request),
        mimetype="application/" + rtype)


def getStikies(request, hiddens, sfrom, to):
    sticky_objs = market.models.MarketItemStick.objects.filter(viewer_id=request.user.id)
    if request.GET.get('showHidden', 'false') == 'false':
        sticky_objs = sticky_objs.filter(~Q(item_id__in=hiddens))
    if request.GET.has_key('types'):
        sticky_objs = sticky_objs.filter(Q(item__item_type__in=request.GET.getlist('types')))
    sticky_objs = sticky_objs[sfrom:to]
    obj = [i.item for i in sticky_objs]
    return obj


def get_raw(request, filter_by_owner=False):
    params = {
        'countries': tuple(map(int, request.GET.getlist('countries', (0,)))),
        'issues': tuple(map(int, request.GET.getlist('issues', (0,)))),
        'skills': tuple(map(int, request.GET.getlist('skills', (0,)))),
        'types': tuple(request.GET.getlist('types', ('offer', 'request'))),
        'user_id': request.user.id,
        'date_now': datetime.now(),
        'closed_statuses': (
            market.models.MarketItem.STATUS_CHOICES.CLOSED_BY_USER,
            market.models.MarketItem.STATUS_CHOICES.CLOSED_BY_ADMIN)
    }
    additional_filter = ''

    search = request.GET.get('search')
    if search:
        market_items = SearchQuerySet().models(
            market.models.MarketItem).filter(text=search)
        if market_items:
            additional_filter = 'AND mi.id IN %(ids)s'
            params['ids'] = tuple(int(obj.pk) for obj in market_items)

    if request.GET.get('showHidden', 'false') == 'false':
        additional_filter += """
            AND NOT mi.id IN (
                SELECT hiddens.item_id
                FROM market_marketitemhidden AS hiddens
                WHERE hiddens.viewer_id = %(user_id)s)
        """

    if filter_by_owner:
        select = 'SELECT mi.* '
        order_by = 'ORDER BY id DESC , pub_date DESC'
        additional_filter += 'AND auth_user.id = %(user_id)s'
    else:
        select = """
        SELECT mi.*,
               (COUNT(DISTINCT market_marketitem_countries.countries_id) +
                COUNT(DISTINCT market_marketitem_issues.issues_id) +
                COUNT(DISTINCT market_marketitem_skills.skills_id)) as tag_matches
        """
        order_by = 'ORDER BY tag_matches DESC, pub_date DESC'

    raw = select + """
        FROM market_marketitem AS mi
        LEFT JOIN market_marketitem_countries ON
            market_marketitem_countries.marketitem_id = mi.id AND
            market_marketitem_countries.countries_id IN %(countries)s
        LEFT JOIN market_marketitem_issues ON
            market_marketitem_issues.marketitem_id = mi.id AND
            market_marketitem_issues.issues_id IN %(issues)s
        LEFT JOIN market_marketitem_skills ON
            market_marketitem_skills.marketitem_id = mi.id AND
            market_marketitem_skills.skills_id IN %(skills)s
        INNER JOIN "auth_user" ON
            mi.owner_id = "auth_user"."id"
        WHERE
            mi.item_type IN %(types)s
    """ + additional_filter + """ AND
            NOT mi.id IN (
                SELECT stickies."item_id"
                FROM "market_marketitemstick" stickies
                WHERE stickies."viewer_id" = %(user_id)s
            ) AND
            mi.published = True AND
            mi.deleted = False AND
            "auth_user"."is_active" = True AND
            NOT mi.status IN %(closed_statuses)s
        GROUP BY mi.id, mi.item_type, mi.owner_id, mi.staff_owner_id, mi.title,
            mi.details, mi.url, mi.published, mi.pub_date,
            mi.commentcount, mi.ratecount, mi.reportcount, mi.score, mi.deleted,
            mi.status, mi.closed_date, mi.feedback_response
    """ + order_by
    return raw, params


@login_required
def get_marketItem_fromto(request, sfrom, to, rtype):
    reqhash = hash(request.path + str(request.GET))
    retval = items_cache.get(reqhash)
    if retval:
        return retval
    query = market.models.MarketItem.objects.raw(*get_raw(request))
    stickies_count = market.models.MarketItemStick.objects.filter(
        viewer_id=request.user.id).count()
    hidden_items = market.models.MarketItemHidden.objects.values_list(
        'item_id', flat=True).filter(viewer_id=request.user.id)
    to = int(to)
    sfrom = int(sfrom)
    if stickies_count >= to:
        stickies = getStikies(request, hidden_items, sfrom, to)
    elif stickies_count <= sfrom:
        stickies = query[sfrom-stickies_count:to-stickies_count]
    else:
        stickies = list(
            getStikies(request, hidden_items, sfrom, stickies_count))
        market_items = list(query[:to-stickies_count])
        stickies.extend(market_items)
    retval = return_item_list(stickies, rtype, request)
    items_cache.add(reqhash, retval)
    return retval


@login_required
@check_perms_and_get(market.models.MarketItem)
def edit_market_item(request,obj_id,rtype):
    cache.delete('item-'+obj_id)
    cache.delete('translation-'+obj_id)
    items_cache.clear()
    user_items_cache.clear()
    obj = request.obj
    form = item_forms[obj.item_type](request.POST, instance=obj)
    if form.is_valid():
        saveMarketItem(form, obj.item_type, obj.owner)
        update_notifications.delay(obj)
    else:
        return HttpResponseError(json.dumps(get_validation_errors(form)), mimetype="application/"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),
                        mimetype="application"+rtype)


@login_required
@check_perms_and_get(market.models.MarketItem)
def close_market_item(request, obj_id, rtype):
    cache.delete('item-'+obj_id)
    cache.delete('translation-'+obj_id)
    items_cache.clear()
    user_items_cache.clear()
    market_item = request.obj

    questionnaire = Questionnaire.objects.filter(
        market_type=market_item.item_type).first()

    # Convert questionnaire to json structure.
    questions = [
        {
            'question_id': question.pk,
            'question_text': question.question,
            'question_answer': ''
        } for question in questionnaire.questions.all()
    ]
    data = {'questionnaire': {
        'questionnaire_id': questionnaire.pk,
        'questionnaire_title': questionnaire.title,
        'questions': questions
    }}

    if request.method == 'POST':
        form = QuestionnaireForm(request.POST, questionnaire=questionnaire)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            for question in questions:
                answer = cleaned_data['question_%s' % question['question_id']]
                question['question_answer'] = answer

            market_item.feedback_response = data['questionnaire']
            market_item.status = market_item.STATUS_CHOICES.CLOSED_BY_USER
            market_item.save()

            update_notifications.delay(market_item)
            data = {'success': True}
        else:
            return HttpResponseError(
                json.dumps(get_validation_errors(form)),
                mimetype="application/" + rtype)

    return HttpResponse(
        json.dumps(data), mimetype="application" + rtype)


@login_required
@check_perms_and_get(market.models.MarketItem)
def user_get_marketitem(request, obj_id, rtype):
    return return_item_list([request.obj], rtype)


@login_required
def get_user_marketitem_fromto(request, sfrom, to, rtype):
    reqhash = hash(request.path+str(request.GET))
    retval = user_items_cache.get(reqhash)
    if retval:
        return retval
    market_items = market.models.MarketItem.objects.raw(
        *get_raw(request, filter_by_owner=True))[int(sfrom):int(to)]
    retval = return_item_list(market_items, rtype)
    user_items_cache.add(reqhash, retval)
    return retval


@login_required
def get_item_translation(request, obj_id, rtype):
    retval = cache.get('translation-' + obj_id)
    if retval:
        return retval
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'),
                            closed_date=None,
                            pk=obj_id,
                            deleted=False,
                            owner__is_active=True)
    resp = requests.get(
        settings.GOOGLE_TRANS_URL + 'key=' + constance.config.GOOGLE_API_KEY + '&source=ar&target=' + 'en' + '&q=' + obj.details)
    retval = return_item_list([obj], rtype)
    cache.add('translation-' + obj_id, retval)
    return retval


@login_required
def set_rate(request, obj_id, rtype):
    if not request.POST.has_key('score'):
        return HttpResponseError()
    cache.delete('item-' + obj_id)
    items_cache.clear()
    user_items_cache.clear()
    item = \
        market.models.MarketItem.filter(closed_date=None).objects.filter(id=obj_id)[0]
    owner = request.user
    rate = market.models.ItemRate.objects.filter(owner=owner).filter(item=item)
    if len(rate) == 0:
        rate = market.models.ItemRate(owner=owner, item=item)
    else:
        rate = rate[0]
    rate.score = int(request.POST['score'])
    rate.save()
    rate.save_base()
    mark_read_notifications.delay((item.id,), request.user.id)
    return HttpResponse(
        json.dumps({'success': 'true',
                    'score': item.score,
                    'ratecount': item.ratecount
        }),
        mimetype="application/" + rtype)


@login_required
def get_notifications_fromto(request, sfrom, to, rtype):
    notifications = market.models.Notification.objects.filter(user=request.user.id, item__deleted=False)[sfrom:to]
    alist = []
    notification_ids = []
    for notification in notifications:
        alist.append(notification.getDict())
        notification_ids.append(notification.id)
    market.models.Notification.objects.filter(id__in=notification_ids).update(seen=True)
    return HttpResponse(json.dumps({'notifications': alist}),
                        mimetype="application" + rtype)


@login_required
def get_notseen_notifications(request, sfrom, to, rtype):
    notifications = market.models.Notification.objects.filter(user=request.user.id, item__deleted=False).filter(
        seen=False).only('seen')
    if len(notifications) > 0:
        return HttpResponse(json.dumps({'result': True}),
                            mimetype="application" + rtype)
    return HttpResponse(json.dumps({'result': False}),
                        mimetype="application" + rtype)


@login_required
def get_views_count(request, obj_id, rtype):
    views = market.models.MarketItemViewConter.objects.filter(item_id=obj_id).count()
    return HttpResponse(json.dumps({'result': views}),
                        mimetype="application" + rtype)


@login_required
def hide_item(request, obj_id, rtype):
    new_hidden = market.models.MarketItemHidden.objects.get_or_create(viewer_id=request.user.id, item_id=obj_id)[0]
    new_hidden.save()
    return HttpResponse(json.dumps({'result': True}),
                        mimetype="application" + rtype)


@login_required
def unhide_item(request, obj_id, rtype):
    result = False
    hidden = market.models.MarketItemHidden.objects.get(viewer_id=request.user.id, item_id=obj_id)
    if hidden:
        hidden.delete()
        result = True
    return HttpResponse(json.dumps({'result': result}),
                        mimetype="application" + rtype)


@login_required
def stick_item(request, obj_id, rtype):
    new_sticky = market.models.MarketItemStick.objects.get_or_create(viewer_id=request.user.id, item_id=obj_id)[0]
    new_sticky.save()
    return HttpResponse(json.dumps({'result': True}),
                        mimetype="application" + rtype)


@login_required
def unstick_item(request, obj_id, rtype):
    result = False
    sticky = market.models.MarketItemStick.objects.get(viewer_id=request.user.id, item_id=obj_id)
    if sticky:
        sticky.delete()
        result = True
    return HttpResponse(json.dumps({'result': result}),
                        mimetype="application" + rtype)
