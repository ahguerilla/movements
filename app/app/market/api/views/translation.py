import json
from datetime import datetime
import itertools

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils import translation as django_translation
from django.utils.translation import ugettext

from app.market.models import TranslationBase, MarketItemTranslation
from app.market.models.translation import get_or_create_translation, get_or_create_user_translation
from app.celerytasks import (
    takein_notification, approved_notification, approve_notification,
    revoke_notification, takeoff_notification
)




@login_required
def translate(request, object_id, model):
    lang_code = request.GET.get('lang_code', django_translation.get_language())
    translation = None

    item = model.get_object(object_id)
    result = {'response': 'error',
              'status': model.global_state.GOOGLE,
              'source_language': item.language,
              'lang_code': lang_code,
              'human_aviable': False,
              'itemid': object_id}

    if item.language == lang_code:
        result.update(model.get_original(item))
        result.update({
            'response': 'success',
        })
        return HttpResponse(json.dumps(result), mimetype="application/json")

    try:
        human_translation = model.objects.get(status=model.global_state.DONE, **model.get_params(object_id, lang_code))
    except model.DoesNotExist:
        human_translation = None

    if human_translation:
        result.update({
            'human_aviable': True,
            'human_translator': human_translation.owner.username,
        })

    if request.GET.get('human', 'true') != 'false' and human_translation is not None:
        result.update({'status': human_translation.status})
        translation = human_translation

    if translation is None:
        translation = get_or_create_translation(object_id, lang_code, model)

    if translation:
        result.update(translation.get_translated_data())
        result.update({'response': 'success'})
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def take_in(request, object_id, model):
    lang_code = request.POST['lang_code']
    result = {'response': 'error', 'id': object_id}
    translation = get_or_create_user_translation(object_id, lang_code, model)
    if not translation.has_perm(request.user, lang_code):
        result.update({'error': ugettext('You do not currently have permissions to translate this item')})
        return HttpResponse(json.dumps(result), mimetype="application/json")
    if translation.c_status == translation.inner_state.NONE:
        translation.take_in(request.user)
        takein_notification.delay(translation, translation.is_done())
        result.update({'response': 'success'})
    elif translation.c_status == translation.inner_state.APPROVAL and request.user.userprofile.is_cm:
        result.update({'response': 'success'})
    elif translation.owner_candidate == request.user:
        result.update({'response': 'success'})
    else:
        force = request.POST.get('force', None)
        if request.user.userprofile.is_cm and force == '1':
            translation.take_in(request.user)
            result.update({'response': 'success'})
        else:
            result.update({
                'error': ugettext('Another user is currently translating this item'),
                'other_user_editing': True
            })
    result.update({
        'user_is_owner': request.user.id == translation.owner_candidate.id,
    })

    if result['response'] == 'success':
        result.update(translation.get_init_data(request.user))
        if request.user.userprofile.is_cm:
            result.update(translation.cm_urls_dict())
    else:
        result.update({
            'status': 0,
            'active': False,
        })
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def save_draft(request, object_id, model):
    lang_code = request.POST['lang_code']
    result = {'response': 'error'}
    try:
        translation = model.objects.get(
            c_status__in=[model.inner_state.TRANSLATION, model.inner_state.CORRECTION],
            owner_candidate=request.user,
            **model.get_params(object_id, lang_code))
        if not translation.has_perm(request.user, lang_code):
            result.update({'error': ugettext('You do not currently have permissions to translate this item')})
            return HttpResponse(json.dumps(result), mimetype="application/json")
        translation.save_draft(request.POST)
        result.update({'response': 'success',
                       'message': ugettext('Draft saved successfully.')})
        result.update(translation.get_init_data(request.user))
    except model.DoesNotExist:
        result['error'] = ugettext('This post is not currently locked for translation.')
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def take_off(request, object_id, model):
    lang_code = request.POST['lang_code']
    result = {'response': 'error'}
    try:
        translation = model.objects.get(
            c_status__in=[model.inner_state.TRANSLATION, model.inner_state.CORRECTION],
            owner_candidate=request.user,
            **model.get_params(object_id, lang_code))
        takeoff_notification.delay(translation)
        translation.clear_state()
        result.update({'response': 'success'})
    except model.DoesNotExist:
        result.update({'error': ugettext('No pending translation found to cancel.')})
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def done(request, object_id, model):
    lang_code = request.POST['lang_code']
    result = {'response': 'error'}
    try:
        translation = model.objects.get(
            c_status__in=[model.inner_state.TRANSLATION, model.inner_state.CORRECTION],
            owner_candidate=request.user,
            **model.get_params(object_id, lang_code))
        translation.set_done(request.POST)
        approve_notification.delay(translation)
        result.update({'response': 'success'})
        if request.user.userprofile.is_cm:
            result.update(translation.cm_urls_dict())
    except model.DoesNotExist:
        result.update({'error': ugettext('This post is not currently locked for translation.')})
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def put_back_to_edit(request, object_id, model):
    lang_code = request.POST['lang_code']
    result = {'response': 'error'}
    try:
        translation = model.objects.get(
            c_status__in=[model.inner_state.APPROVAL, model.inner_state.CORRECTION, model.inner_state.TRANSLATION],
            owner_candidate=request.user,
            **model.get_params(object_id, lang_code))
        if not translation.has_perm(request.user, lang_code):
            result.update({'error': ugettext('You do not currently have permissions to translate this item')})
            return HttpResponse(json.dumps(result), mimetype="application/json")
        translation.set_to_edit()
        result.update(translation.get_init_data(request.user))
        result.update({'response': 'success'})
    except model.DoesNotExist:
        result.update({'error': ugettext('This post is not currently locked for translation.')})
    return HttpResponse(json.dumps(result), mimetype="application/json")


def _approve_correct_revoke(request, object_id, lang_code, model, params):
    params.update(model.get_params(object_id, lang_code))
    translation = None
    result = {'response': 'error'}
    if not request.user.userprofile.is_cm:
        result.update({'error': ugettext('You do not have permission to complete this action.')})
    else:
        try:
            translation = model.objects.get(**params)
        except model.DoesNotExist:
            result.update({'error': 'Translation record not found.'})
    return result, translation


@require_http_methods(['POST'])
@login_required
def approve(request, object_id, model):
    lang_code = request.POST['lang_code']
    params = {'status__gte': TranslationBase.global_state.PENDING,
              'c_status': TranslationBase.inner_state.APPROVAL}
    result, translation = _approve_correct_revoke(request, object_id, lang_code, model, params)
    if translation:
        translation.approve(request.POST)
        approved_notification.delay(translation)
        translation.clear_state()
        result.update({'response': 'success'})
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def corrections(request, object_id, model):
    lang_code = request.POST['lang_code']
    params = {'status__gte': TranslationBase.global_state.PENDING,
              'c_status': TranslationBase.inner_state.APPROVAL}
    result, translation = _approve_correct_revoke(request, object_id, lang_code, model, params)
    if translation:
        translation.c_status = translation.inner_state.CORRECTION
        translation.timer = datetime.utcnow()
        translation.save()
        takein_notification.delay(translation, True)
        result.update({'response': 'success'})

    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def revoke(request, object_id, model):
    lang_code = request.POST['lang_code']
    params = {'status__gte': TranslationBase.global_state.PENDING,
              'c_status__gt': TranslationBase.inner_state.NONE}
    result, translation = _approve_correct_revoke(request, object_id, lang_code, model, params)
    if translation:
        revoke_notification.delay(translation)
        translation.clear_state()
        result.update({'response': 'success'})
    return HttpResponse(json.dumps(result), mimetype="application/json")


def _market_translation_for_json(item):
    return {
        'title': item.market_item.title,
        'type': 'post',
        'from_code': item.source_language,
        'to_code': item.language,
        'title_candidate': item.title_candidate,
        'item_url': reverse('show_post', args=[item.market_item.id]),
    }


@require_http_methods(['GET'])
@login_required
def claimed_translations(request):
    if not request.user.userprofile.is_translator:
        raise ValueError
    market_item_translations = MarketItemTranslation \
        .objects \
        .select_related('market_item') \
        .filter(owner_candidate=request.user,
                c_status__in=[TranslationBase.inner_state.TRANSLATION,
                              TranslationBase.inner_state.APPROVAL,
                              TranslationBase.inner_state.CORRECTION])
    translations = [_market_translation_for_json(t) for t in market_item_translations]
    return HttpResponse(json.dumps({'translations': translations}), mimetype="application/json")


@require_http_methods(['GET'])
@login_required
def available_translations(request):
    if not request.user.userprofile.is_translator:
        raise ValueError
    market_item_translations = MarketItemTranslation \
        .objects \
        .select_related('market_item') \
        .filter(c_status=TranslationBase.inner_state.NONE,
                status=TranslationBase.global_state.PENDING)
    languages = request.user.userprofile.translation_languages.all()
    for permutation in itertools.permutations(languages, 2):
        market_item_translations = market_item_translations.filter(source_language=permutation[0],
                                                                   language=permutation[1])
    translations = [_market_translation_for_json(t) for t in market_item_translations]
    return HttpResponse(json.dumps({'translations': translations}), mimetype="application/json")
