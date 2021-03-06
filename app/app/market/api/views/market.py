import json
import math
from datetime import datetime
import bleach

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import connection
from django.db.models import Q

from haystack.query import SearchQuerySet

from app.utils import form_errors_as_dict
from app.market.api.utils import *
import app.market as market
from app.market.models import Questionnaire
from app.market.forms import QuestionnaireForm, NewsOfferForm
from app.celerytasks import update_notifications


def get_market_json(items, request=None, extra_data=None, is_safe=True):
    if is_safe:
        to_json = [item.getdict_safe() for item in items]
    else:
        to_json = [item.getdict(request) for item in items]
    if extra_data:
        to_json.append(extra_data)
    return json.dumps(to_json)


def return_item_list(obj, rtype='json', request=None, is_safe=True):
    return HttpResponse(
        get_market_json(obj, request, is_safe=is_safe),
        mimetype="application/" + rtype)


def get_raw(request, from_item=0, to_item=None,
            filter_by_owner=False, count=False, user_id=None):
    skills = map(int, request.GET.getlist('skills', []))
    issues = map(int, request.GET.getlist('issues', []))
    show_other_skills = -1 in skills
    show_other_issues = -1 in issues

    countries = map(int, request.GET.getlist('countries', []))
    params = {
        'interests': tuple(skills),
        'issues': tuple(issues),
        'countries': tuple(countries),
        'types': tuple(request.GET.getlist('types', ('offer', 'request', 'news'))),
        'user_id': user_id if user_id else request.user.id,
        'date_now': datetime.utcnow(),
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
        additional_filter = 'AND mi.id IN %(ids)s'
        market_items = SearchQuerySet().models(market.models.MarketItem).filter(text=search)
        if market_items:
            params['ids'] = tuple(int(obj.pk) for obj in market_items)
        else:
            params['ids'] = (-1,)

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
            AND (EXISTS
                    (SELECT * FROM market_marketitem_interests
                     WHERE market_marketitem_interests.marketitem_id = mi.id AND
                          market_marketitem_interests.interest_id IN %(interests)s
                     )
        """
        if show_other_skills:
            additional_filter += """
                        OR (mi.specific_skill IS NOT NULL AND length(mi.specific_skill) > 0))
                    """
        else:
            additional_filter += ')'

    if issues:
        additional_filter += """
            AND (EXISTS
                    (SELECT * FROM market_marketitem_issues
                     WHERE market_marketitem_issues.marketitem_id = mi.id AND
                          market_marketitem_issues.issues_id IN %(issues)s
                     )
        """
        if show_other_issues:
            additional_filter += """
                OR (mi.specific_issue IS NOT NULL AND length(mi.specific_issue) > 0))
            """
        else:
            additional_filter += ')'

    if countries:
        additional_filter += """
            AND EXISTS (
                SELECT * FROM market_marketitem_countries
                WHERE market_marketitem_countries.marketitem_id = mi.id AND
                      market_marketitem_countries.countries_id IN %(countries)s
            )
        """

    select = """SELECT mi.*,
                (SELECT image
                 FROM market_marketitemimage
                 WHERE market_marketitemimage.item_id = mi.id ORDER BY id DESC limit 1) AS image_url"""
    if filter_by_owner:
        order_by = ' ORDER BY id DESC , pub_date DESC'
        additional_filter += 'AND auth_user.id = %(user_id)s'
    else:
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
    market_json = get_market_json(market_items, request, is_safe=False)
    return HttpResponse(market_json, mimetype='application/json')


@login_required
def get_market_items_user(request, user_id=None):
    if not user_id:
        user_id = request.user.id
    return get_market_items(request, user_id=user_id, filter_by_user=True)


def get_market_items(request, user_id=None, filter_by_user=False):
    page = int(request.GET.get('page', 1))
    market_items_count = get_item_count(request, user_id=user_id, filter_by_user=filter_by_user)
    max_page_num = math.ceil(market_items_count / float(settings.PAGE_SIZE))
    max_page_num = max(max_page_num, 1)
    # page_num = min(page, max_page_num)
    # Removed for infinite scroll (Now returns zero items once beyond last page)
    page_num = page
    from_item = (page_num - 1) * settings.PAGE_SIZE
    to_item = from_item + settings.PAGE_SIZE

    market_items = list(market.models.MarketItem.objects.raw(
        *get_raw(request, from_item, to_item, filter_by_owner=filter_by_user, user_id=user_id)))

    is_safe = True
    if request.user.is_authenticated():
        is_safe = False

    market_json = get_market_json(market_items, request, {'page_count': max_page_num, 'current_page': page_num,
                                                          'page_size': settings.PAGE_SIZE}, is_safe=is_safe)
    return HttpResponse(market_json, mimetype='application/json')


def get_featured_market_items(request):
    featured_posts = market.models.MarketItem.objects.exclude(
        status__in=[market.models.MarketItem.STATUS_CHOICES.CLOSED_BY_USER,
                    market.models.MarketItem.STATUS_CHOICES.CLOSED_BY_ADMIN])\
        .filter(is_featured=True).order_by('featured_order_hint')

    is_safe = True
    if request.user.is_authenticated():
        is_safe = False

    return return_item_list(featured_posts, request=request, is_safe=is_safe)


@login_required
@require_POST
def unpublish_market_item(request, obj_id):
    market_item = get_object_or_404(market.models.MarketItem, pk=obj_id)
    if request.user != market_item.owner:
        return HttpResponseForbiden()
    market_item.published = False
    market_item.save()
    return HttpResponse(json.dumps({'success': True}), mimetype="application/json")


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

    return HttpResponse(json.dumps(data), mimetype="application/json")


def get_marketitems_fromto(request, sfrom, to, rtype):
    market_items = market.models.MarketItem.objects.raw(
        *get_raw(request, filter_by_owner=False))[int(sfrom):int(to)]
    retval = return_item_list(market_items, rtype, request, is_safe=False)
    return retval


@login_required
def get_user_marketitem_fromto(request, sfrom, to, rtype):
    market_items = market.models.MarketItem.objects.raw(
        *get_raw(request, filter_by_owner=True))[int(sfrom):int(to)]
    retval = return_item_list(market_items, rtype, request, is_safe=False)
    return retval


@login_required
def get_user_marketitem_for_user_fromto(request, user_id, sfrom, to, rtype):
    market_items = market.models.MarketItem.objects.raw(
        *get_raw(request, filter_by_owner=True, user_id=user_id))[int(sfrom):int(to)]
    return return_item_list(market_items, rtype, request, is_safe=False)


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
    return HttpResponse(
        json.dumps({'success': 'true',
                    'score': item.score,
                    'ratecount': item.ratecount
        }),
        mimetype="application/" + rtype)


@login_required
def get_notifications_fromto(request, sfrom, to):
    query = (Q(item__deleted=False) | Q(item=None)) & Q(user_id=request.user.id)
    notifications = market.models.Notification.objects.filter(query)[sfrom:to]
    ret_list = []
    for notification in notifications:
        ret_list.append(notification.get_dict())
    market.models.Notification.objects.filter(user_id=request.user.id).update(seen=True)
    return HttpResponse(json.dumps({'notifications': ret_list}), mimetype="application/json")


@login_required
def get_notseen_notifications(request):
    has_unseen = market.models.Notification.objects.filter(user=request.user.id, item__deleted=False,
                                                           seen=False).exists()
    return HttpResponse(json.dumps({'result': has_unseen}),
                        mimetype="application/json")


@login_required
def set_item_attributes_for_user(request, item_id):
    hide = request.POST.get('hidden', None)
    if hide is not None:
        set_hidden(request.user.id, item_id, hide == 'true')
    stick = request.POST.get('stick', None)
    if stick is not None:
        set_stuck(request.user.id, item_id, stick == 'true')
    return HttpResponse(json.dumps({'result': True}))


@login_required
@require_POST
def offer_help(request, item_id):
    market_item = get_object_or_404(market.models.MarketItem, pk=item_id)
    form = NewsOfferForm(request.POST)
    if form.is_valid():
        offer = form.save(commit=True, market_item=market_item, owner=request.user)
        details = bleach.clean(offer.details, tags=['a', 'img', 'bold', 'strong', 'i', 'em'],
                               attributes=['href', 'title', 'alt', 'src'], strip=True)
        args = {
            'success': True,
            'avatar': reverse('avatar_render_primary', args=(request.user.username, 60)),
            'owner': request.user.username,
            'id': offer.id,
            'interests': [o.name for o in offer.interests.all()],
            'specific_interest': offer.specific_interest if offer.specific_interest else '',
            'details': details,
            'rating': offer.owner.userprofile.ahr_rating,
        }
        return HttpResponse(json.dumps(args), mimetype="application/json")
    errors = form_errors_as_dict(form)
    return HttpResponse(json.dumps({'success': False, 'errors': errors}), mimetype="application/json")


@login_required
@require_POST
def delete_offer_help(request, item_id):
    offer = get_object_or_404(market.models.MarketItemDirectOffer, pk=item_id)
    if offer.owner != request.user:
        raise PermissionDenied
    offer.deleted = True
    offer.save()
    return HttpResponse(json.dumps({'success': True}), mimetype="application/json")


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
