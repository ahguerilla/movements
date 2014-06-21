import json
from datetime import datetime

from django.db.models import Q
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import login_required
from app.market.api.utils import *
import app.market as market
from app.market.models import Questionnaire
from app.market.forms import QuestionnaireForm
from tasks.celerytasks import update_notifications, mark_read_notifications


def get_market_json(objs, request=None):
    alist = []
    for obj in objs:
        alist.append(obj.getdict(request))
    return json.dumps(alist)


def return_item_list(obj, rtype, request=None):
    return HttpResponse(
        get_market_json(obj, request),
        mimetype="application/" + rtype)


def get_stickies(request, hiddens, sfrom, to):
    sticky_objs = market.models.MarketItemStick.objects.filter(viewer_id=request.user.id)
    if request.GET.get('showHidden', 'false') == 'false':
        sticky_objs = sticky_objs.filter(~Q(item_id__in=hiddens))
    if 'types' in request.GET:
        sticky_objs = sticky_objs.filter(Q(item__item_type__in=request.GET.getlist('types')))
    sticky_objs = sticky_objs[sfrom:to]
    obj = [i.item for i in sticky_objs]
    return obj


def get_raw(request, filter_by_owner=False, user_id=None):
    params = {
        'countries': tuple(map(int, request.GET.getlist('countries', (0,)))),
        'issues': tuple(map(int, request.GET.getlist('issues', (0,)))),
        'skills': tuple(map(int, request.GET.getlist('skills', (0,)))),
        'types': tuple(request.GET.getlist('types', ('offer', 'request'))),
        'user_id': user_id if user_id else request.user.id,
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
    query = market.models.MarketItem.objects.raw(*get_raw(request))
    stickies_count = market.models.MarketItemStick.objects.filter(
        viewer_id=request.user.id).count()
    hidden_items = market.models.MarketItemHidden.objects.values_list(
        'item_id', flat=True).filter(viewer_id=request.user.id)
    to = int(to)
    sfrom = int(sfrom)
    if stickies_count >= to:
        stickies = get_stickies(request, hidden_items, sfrom, to)
    elif stickies_count <= sfrom:
        stickies = query[sfrom-stickies_count:to-stickies_count]
    else:
        stickies = list(
            get_stickies(request, hidden_items, sfrom, stickies_count))
        market_items = list(query[:to-stickies_count])
        stickies.extend(market_items)
    retval = return_item_list(stickies, rtype, request)
    return retval


@login_required
@check_perms_and_get(market.models.MarketItem)
def close_market_item(request, obj_id, rtype):
    market_item = request.obj

    questionnaire = Questionnaire.objects.filter(market_type=market_item.item_type).first()

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
def get_user_marketitem_fromto(request, sfrom, to, rtype):
    market_items = market.models.MarketItem.objects.raw(
        *get_raw(request, filter_by_owner=True))[int(sfrom):int(to)]
    retval = return_item_list(market_items, rtype)
    return retval


@login_required
def get_user_marketitem_for_user_fromto(request, user_id, sfrom, to, rtype):
    market_items = market.models.MarketItem.objects.raw(
        *get_raw(request, filter_by_owner=True, user_id=user_id))[int(sfrom):int(to)]
    return return_item_list(market_items, rtype)


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
