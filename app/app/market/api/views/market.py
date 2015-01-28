import json
import math
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import connection
from django.db.models import Q
from haystack.query import SearchQuerySet

from app.market.api.utils import *
import app.market as market
from app.market.models import Questionnaire
from app.market.forms import QuestionnaireForm
from tasks.celerytasks import (
    update_notifications, takein_notification, takeoff_notification,
    correction_notification, approved_notification, approve_notification)
from app.market.api.utils import translate_text
import bleach


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
    countries = map(int, request.GET.getlist('countries', []))
    params = {
        'interests': tuple(skills),
        'countries': tuple(countries),
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
            AND EXISTS (
                SELECT * FROM market_marketitem_interests
                WHERE market_marketitem_interests.marketitem_id = mi.id AND
                      market_marketitem_interests.interest_id IN %(interests)s
            )
        """

    if countries:
        additional_filter += """
            AND EXISTS (
                SELECT * FROM market_marketitem_countries
                WHERE market_marketitem_countries.marketitem_id = mi.id AND
                      market_marketitem_countries.countries_id IN %(countries)s
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
                    market.models.MarketItem.STATUS_CHOICES.CLOSED_BY_ADMIN]).filter(is_featured=True)

    is_safe = True
    if request.user.is_authenticated():
        is_safe = False

    return return_item_list(featured_posts, request=request, is_safe=is_safe)


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


def get_or_create_item_translation(item_id, lang_code):
    translation = market.models.MarketItemTranslation.objects.filter(
            status=market.models.MarketItemTranslation.STATUS_CHOICES.GOOGLE,
            market_item_id=item_id, language=lang_code).first()
    if translation:
        return translation

    item = market.models.MarketItem.objects.get(id=item_id)
    if item:
        success, title_translation, source_lang = translate_text(item.title, lang_code)
        if success:
            success, details_translation, source_lang = translate_text(item.details, lang_code)
        if success:
            translation = market.models.MarketItemTranslation.objects.create(
            market_item=item,
            title_translated=title_translation,
            details_translated = details_translation,
            language = lang_code,
            source_language = source_lang)
            return translation
    return False


@login_required
def translate_market_item(request, item_id, lang_code):
    # find out if the translation already exists
    # by default is looking for human translation
    params = {'market_item_id': item_id, 'language': lang_code}
    states = market.models.MarketItemTranslation.STATUS_CHOICES
    translation = None
    title_translation = ""
    details_translation = ""
    status = states.GOOGLE
    human_aviable = False
    source_lang = ""
    success = False

    if request.GET.get('human', True) == True:
        try:
            translation = market.models.MarketItemTranslation.objects.get(
                status__gt=states.PENDING,
                **params)
            status = translation.status
            human_aviable = True
        except Exception as e:
            print(e)
    elif market.models.MarketItemTranslation.objects.filter(
       status=states.DONE,
       **params).exists():
        human_aviable = True

    if status < states.DONE:
        translation = get_or_create_item_translation(item_id, lang_code)

    if translation:
        title_translation = translation.title_translated
        details_translation = translation.details_translated
        source_lang = translation.source_language
        success = True

    result = {
        'response': "success" if success else "failed",
        'title': bleach.clean(title_translation, strip=True),
        'details': bleach.clean(details_translation, strip=True),
        'source_language': source_lang,
        'itemid': item_id,
        'status': status,
        'human_aviable': human_aviable,
        'username': translation.owner.username if status == states.DONE else 'Google'
    }
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['GET'])
@login_required
def translate_market_item_init(request, item_id, lang_code):
    # market.models.MarketItemTranslation.objects.all().delete()
    # market.models.TraslationCandidade.objects.all().delete()

    translation = None
    result = {
        'response': 'success',
        'active': False,
        'status': False,
        'owner': None,
        'take_in_url': reverse('take_in_translate_item', args=(item_id, lang_code)),
        'take_off_url': None,
        }

    try:
        translation = market.models.MarketItemTranslation.objects.get(
            status__gte=market.models.MarketItemTranslation.STATUS_CHOICES.PENDING,
            market_item_id=item_id, language=lang_code)
        result.update({
            'correction': translation.is_done(),
            })
    except:
        pass

    if translation:
        result.update({
            'prev_title': translation.title_translated,
            'prev_text': translation.details_translated})

        try:
            candidate = market.models.TraslationCandidade.objects.get(
                translation=translation, market_item_id=item_id)
            active = candidate.is_active(request.user)
            result.update({
                'active': active,
                'owner': candidate.owner.username,
                'status': candidate.status,
                'details_translated': candidate.details_translated,
                'title_translated': candidate.title_translated,
                'take_off': candidate.take_off_url() if active else None,
                'done_url': candidate.done_url() if active else None,
                'take_in_url': None,
                })

            if candidate.status == candidate.STATUS_CHOICES.APPROVAL and\
               request.user.userprofile.is_cm:
                result.update(candidate.cm_urls_dict())
        except Exception as e:
            pass

    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['GET'])
@login_required
def take_in_translation(request, item_id, lang_code):
    candidate, created = market.models.TraslationCandidade.objects.get_or_create(
        market_item_id=item_id, language=lang_code,
        defaults={'owner': request.user, })

    result = {'response': 'error', 'error': 'Translation is busy'}
    if created:
        candidate.status = market.models.TraslationCandidade.STATUS_CHOICES.ACTIVE
        translation, created = market.models.MarketItemTranslation.objects.get_or_create(
            status__gt=market.models.MarketItemTranslation.STATUS_CHOICES.GOOGLE,
            market_item_id=item_id, language=lang_code,
            defaults={'status': market.models.MarketItemTranslation.STATUS_CHOICES.TRANSLATION})
        if created:
            g_translation = get_or_create_item_translation(item_id, lang_code)
            translation.details_translated = g_translation.details_translated
            translation.title_translated = g_translation.title_translated
            translation.source_language = g_translation.source_language
            translation.save()
        elif translation.is_done():
            translation.owner = request.user
            translation.status = market.models.MarketItemTranslation.STATUS_CHOICES.TRANSLATION
            translation.save()
            candidate.status = market.models.TraslationCandidade.STATUS_CHOICES.CORRECTION
        candidate.details_translated = translation.details_translated
        candidate.title_translated = translation.title_translated
        candidate.translation = translation
        candidate.save()

        # create "take in" notifications
        takein_notification.delay(candidate, translation.is_done())

    active = candidate.is_active(request.user)

    if active:
        result = {
            'response': 'success',
            'active': active,
            'owner': candidate.owner.username,
            'details_translated': translation.details_translated,
            'title_translated': translation.title_translated,
            'status': candidate.status,
            'take_off': candidate.take_off_url() if active else None,
            'done_url': candidate.done_url() if active else None,
            }

    return HttpResponse(json.dumps(result), mimetype="application/json")


@login_required
def take_off(request, item_id, lang_code):
    obj = market.models.TraslationCandidade.objects.filter(
        market_item_id=item_id, language=lang_code,
        owner=request.user)
    takeoff_notification.delay(obj.market_item, lang_code)
    obj.delete()

    result = {
        'response': 'success',
        'take_in_url': reverse('take_in_translate_item', args=(item_id, lang_code)),
        }
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def mark_as_done(request, item_id, lang_code):
    try:
        candidate = market.models.TraslationCandidade.objects.get(
            status__lt=market.models.TraslationCandidade.STATUS_CHOICES.APPROVAL,
            market_item_id=item_id, language=lang_code,
            owner=request.user)
        candidate.details_translated = request.POST.get('details_translated')
        candidate.title_translated = request.POST.get('title_translated')
        candidate.mark_to_approval()
        result = {'response': 'success',}

        if request.user.userprofile.is_cm:
            result.update(candidate.cm_urls_dict())
        approve_notification.delay(candidate)

    except Exception as e:
        result = {'response': 'error'}
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def approve_translation(request, item_id, lang_code):
    if not request.user.userprofile.is_cm:
        return HttpResponseForbiden()
    try:
        candidate = market.models.TraslationCandidade.objects.get(
            status=market.models.TraslationCandidade.STATUS_CHOICES.APPROVAL,
            market_item_id=item_id, language=lang_code
            )
        candidate.translation.details_translated = request.POST.get(
            'details_translated', candidate.details_translated)
        candidate.translation.title_translated = request.POST.get(
            'title_translated', candidate.title_translated)
        candidate.translation.status = market.models.MarketItemTranslation.STATUS_CHOICES.DONE
        candidate.translation.save()
        approved_notification.delay(candidate)
        candidate.delete()
        status = True
    except Exception as e:
        print(e)
        status = False

    result = {'response': 'success' if status else 'error'}

    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['GET'])
@login_required
def revoke_translation(request, item_id, lang_code):
    if not request.user.userprofile.is_cm:
        return HttpResponseForbiden()
    try:
        candidate = market.models.TraslationCandidade.objects.get(
            status=market.models.TraslationCandidade.STATUS_CHOICES.APPROVAL,
            market_item_id=item_id, language=lang_code
            )
        candidate.translation.set_done_or_pending()
        takeoff_notification.delay(candidate.market_item, lang_code)
        candidate.delete()
        status = True
    except Exception as e:
        print(e)
        status = False

    result = {'response': 'success' if status else 'error'}

    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def request_corrections_translation(request, item_id, lang_code):
    if not request.user.userprofile.is_cm:
        return HttpResponseForbiden()
    try:
        candidate = market.models.TraslationCandidade.objects.get(
            status=market.models.TraslationCandidade.STATUS_CHOICES.APPROVAL,
            market_item_id=item_id, language=lang_code
            )
        candidate.status = candidate.STATUS_CHOICES.CORRECTION
        candidate.save()
        correction_notification.delay(candidate)
        status = True
    except Exception as e:
        print(e)
        status = False

    result = {'response': 'success' if status else 'error'}

    return HttpResponse(json.dumps(result), mimetype="application/json")
