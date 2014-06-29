import json
import math
from datetime import datetime

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import connection
from haystack.query import SearchQuerySet

from app.market.api.utils import *
import app.market as market
from app.market.models import Questionnaire
from app.market.forms import QuestionnaireForm
from tasks.celerytasks import update_notifications, mark_read_notifications


def get_market_json(items, request=None, extra_data=None):
    to_json = [item.getdict(request) for item in items]
    if extra_data:
        to_json.append(extra_data)
    return json.dumps(to_json)


def return_item_list(obj, rtype='json', request=None):
    return HttpResponse(
        get_market_json(obj, request),
        mimetype="application/" + rtype)


def get_raw(request, from_item=0, to_item=None,
            filter_by_owner=False, count=False, user_id=None):
    skills = map(int, request.GET.getlist('skills', []))
    params = {
        'interests': tuple(skills),
        'types': tuple(request.GET.getlist('types', ('offer', 'request'))),
        'user_id': user_id if user_id else request.user.id,
        'date_now': datetime.now(),
        'closed_statuses': (
            market.models.MarketItem.STATUS_CHOICES.CLOSED_BY_USER,
            market.models.MarketItem.STATUS_CHOICES.CLOSED_BY_ADMIN),
        'offset': from_item,
    }
    additional_filter = ''

    if to_item:
        params['limit'] = to_item - from_item
        limit = ' LIMIT %(limit)s'
    else:
        limit = ''

    search = request.GET.get('search')
    if search:
        market_items = SearchQuerySet().models(market.models.MarketItem).filter(text=search)
        if market_items:
            additional_filter = 'AND mi.id IN %(ids)s'
            params['ids'] = tuple(int(obj.pk) for obj in market_items)

    if request.GET.get('showHidden', 'false') == 'false':
        additional_filter += """
            AND NOT EXISTS (
                SELECT *
                FROM market_marketitemhidden
                WHERE market_marketitemhidden.item_id = mi.id AND
                      market_marketitemhidden.viewer_id = %(user_id)s
            )
        """

    if skills:
        additional_filter += """
            AND EXISTS (
                SELECT * FROM market_marketitem_interests
                WHERE market_marketitem_interests.marketitem_id = mi.id AND
                      market_marketitem_interests.interest_id IN %(interests)s
            )
        """

    if filter_by_owner:
        select = 'SELECT mi.* '
        order_by = ' ORDER BY id DESC , pub_date DESC'
        additional_filter += 'AND auth_user.id = %(user_id)s'
    else:
        select = """SELECT mi.*"""
        order_by = ' ORDER BY pub_date DESC'

    if count:
        select = 'SELECT COUNT(DISTINCT mi.id) '
        group_by = ''
        order_by = ''
    else:
        group_by = ' GROUP BY mi.id'

    raw = select + """
        FROM market_marketitem AS mi
        INNER JOIN "auth_user" ON
            mi.owner_id = "auth_user"."id"
        WHERE
            mi.item_type IN %(types)s
    """ + additional_filter + """ AND
            mi.published = True AND
            mi.deleted = False AND
            "auth_user"."is_active" = True AND
            NOT mi.status IN %(closed_statuses)s
        """ + group_by + order_by + ' OFFSET %(offset)s' + limit
    return raw, params


def get_item_count(request, user_id=None, filter_by_user=False):
    cursor = connection.cursor()
    cursor.execute(*get_raw(request, count=True, user_id=user_id, filter_by_owner=filter_by_user))
    return cursor.fetchone()[0]


@login_required
def get_user_stickies(request):
    market_items = market.models.MarketItem.objects.filter(marketitemstick__viewer_id=request.user.id)
    market_json = get_market_json(market_items, request)
    return HttpResponse(market_json, mimetype='application/json')


@login_required
def get_market_items_user(request, user_id=None):
    if not user_id:
        user_id = request.user.id
    return get_market_items(request, user_id=user_id, filter_by_user=True)


@login_required
def get_market_items(request, user_id=None, filter_by_user=False):
    page = int(request.GET.get('page', 1))
    market_items_count = get_item_count(request, user_id=user_id, filter_by_user=filter_by_user)
    max_page_num = math.ceil(market_items_count / float(settings.PAGE_SIZE))
    max_page_num = max(max_page_num, 1)
    page_num = min(page, max_page_num)
    from_item = (page_num - 1) * settings.PAGE_SIZE
    to_item = from_item + settings.PAGE_SIZE

    market_items = list(market.models.MarketItem.objects.raw(
        *get_raw(request, from_item, to_item, filter_by_owner=filter_by_user, user_id=user_id)))

    market_json = get_market_json(market_items, request, {'page_count': max_page_num, 'current_page': page_num,
                                                          'page_size': settings.PAGE_SIZE})
    return HttpResponse(market_json, mimetype='application/json')


@login_required
def get_featured_market_items(request):
    featured_posts = market.models.MarketItem.objects.exclude(
        status__in=[market.models.MarketItem.STATUS_CHOICES.CLOSED_BY_USER,
                    market.models.MarketItem.STATUS_CHOICES.CLOSED_BY_ADMIN]).filter(is_featured=True)
    return return_item_list(featured_posts, request=request)


@login_required
@check_perms_and_get(market.models.MarketItem)
def close_market_item(request, obj_id):
    market_item = request.obj

    questionnaire = Questionnaire.objects.filter(market_type=market_item.item_type).first()

    # Convert questionnaire to json structure.
    questions = [
        {
            'question_id': question.pk,
            'question_type': question.question_type,
            'question_text': question.question,
            'question_answer': ''
        } for question in questionnaire.questions.all()
    ]

    questions.sort(key=lambda x: x["question_id"], reverse=False)

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
                mimetype="application/json")

    return HttpResponse(
        json.dumps(data), mimetype="application/json")


@login_required
def get_user_marketitem_fromto(request, sfrom, to, rtype):
    market_items = market.models.MarketItem.objects.raw(
        *get_raw(request, filter_by_owner=True))[int(sfrom):int(to)]
    retval = return_item_list(market_items, rtype, request)
    return retval


@login_required
def get_user_marketitem_for_user_fromto(request, user_id, sfrom, to, rtype):
    market_items = market.models.MarketItem.objects.raw(
        *get_raw(request, filter_by_owner=True, user_id=user_id))[int(sfrom):int(to)]
    return return_item_list(market_items, rtype, request)


@login_required
def set_rate(request, obj_id, rtype):
    if not request.POST.has_key('score'):
        return HttpResponseError()
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
def set_item_attributes_for_user(request, item_id):
    hide = request.POST.get('hidden', None)
    if hide is not None:
        set_hidden(request.user.id, item_id, hide == 'true')
    stick = request.POST.get('stick', None)
    if stick is not None:
        set_stuck(request.user.id, item_id, stick == 'true')
    return HttpResponse(json.dumps({'result': True}))


def set_hidden(user_id, item_id, hide):
    if hide:
        market.models.MarketItemHidden.objects.get_or_create(viewer_id=user_id, item_id=item_id)
    else:
        market.models.MarketItemHidden.objects.filter(viewer_id=user_id, item_id=item_id).delete()


def set_stuck(user_id, item_id, stick):
    if stick:
        market.models.MarketItemStick.objects.get_or_create(viewer_id=user_id, item_id=item_id)
    else:
        market.models.MarketItemStick.objects.filter(viewer_id=user_id, item_id=item_id).delete()
