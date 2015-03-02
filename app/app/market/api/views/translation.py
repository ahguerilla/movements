import json
# import bleach
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from app.users.models import LanguageRating
from app.market.models import (
    TranslationBase, CommentTranslation, MarketItemTranslation)
from tasks.celerytasks import (
    takein_notification, approved_notification, approve_notification,
    revoke_notification, takeoff_notification
    )


def get_or_create_translation(object_id, lang_code, model):
    # model must be TranslationBase class or child
    translation = None
    try:
        translation = model.objects.get(
            status=model.global_state.GOOGLE,
            **model.get_params(object_id, lang_code))
    except model.DoesNotExist:
        translation = model.create_translation(object_id, lang_code)
    return translation


def get_or_create_user_translation(object_id, lang_code, model):
    # model must be TranslationBase class or child
    try:
        translation = model.objects.get(
            status__gte=model.global_state.PENDING,
            **model.get_params(object_id, lang_code))
    except model.DoesNotExist:
        translation = get_or_create_translation(object_id, lang_code, model)
        if translation:
            translation.pk = None
            translation.status = model.global_state.PENDING
            translation.save()
    return translation


@login_required
def translate(request, object_id, lang_code, model):
    # model must be TranslationBase class or child
    # find out if the translation already exists
    # by default is looking for human translation
    translation = None
    result = {'response': 'error',
              'status': model.global_state.GOOGLE,
              'source_language': '',
              'human_aviable': False,
              'itemid': object_id}

    if request.GET.get('human', True) == True:
        try:
            translation = model.objects.get(
                status__gt=model.global_state.PENDING,
                **model.get_params(object_id, lang_code))
            result.update({'status': translation.status,
                           'human_aviable': True})
        except model.DoesNotExist:
            pass
    elif model.objects.filter(
       status=model.global_state.DONE,
       **model.get_params(object_id, lang_code)).exists():
        result.update({'human_aviable': True})

    if result.get('status') < model.global_state.DONE:
        translation = get_or_create_translation(object_id, lang_code, model)

    if translation:
        result.update(translation.get_translated_data())
        result.update({'response': 'success'})
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def pre_init(request, model):
    # model must be Comment or MarketItem class
    # returns list of aviable languages to init translation
    result = {
        'response': 'error',
        'error': 'has no permission',
    }
    languages = []
    try:
        object_id = request.POST.get('object_id', None)
        if object_id is None:
            raise model.DoesNotExist
        _object = model.objects.get(pk=object_id)
    except model.DoesNotExist:
        result.update({'error': 'invalid object_id ID'})
    else:
        if request.user.userprofile.is_cm:
            for language in request.user.userprofile.languages.exclude(launguage_code=_object.language):
                languages.append({
                    'name': language.name,
                    'url': _object.init_url(language.launguage_code)
                    })
        else:
            try:
                source_rate = LanguageRating.objects.get(
                    user_id=request.user.pk, language__launguage_code=_object.language
                    )
            except LanguageRating.DoesNotExist:
                print(_object.language)
            else:
                rates = LanguageRating.objects\
                    .filter(user_id=request.user.pk)\
                    .exclude(pk=source_rate.pk)\
                    .values('rate', 'language__launguage_code', 'language__name')
                if rates:
                    for rate in rates:
                        if rate['rate'] + source_rate.rate > 3:
                            languages.append({
                                'name': rate['language__name'],
                                'url': _object.init_url(rate['language__launguage_code'])
                                })
    if len(languages) > 0:
        del result['error']
        result.update({'response': 'success',
                       'languages': languages})

    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['GET'])
@login_required
def init(request, object_id, lang_code, model):
    # model must be TranslationBase class or child
    translation = None
    result = {'response': 'error',
              'id': object_id}

    translation = get_or_create_user_translation(object_id, lang_code, model)
    if not translation:
        return HttpResponse(json.dumps(result), mimetype="application/json")

    if translation.has_perm(request.user, lang_code) and \
       translation.c_status == translation.inner_state.NONE:
        result.update({'take_in_url': translation.take_in_url(lang_code)})

    result.update(translation.get_init_data(request.user))
    result.update({'response': 'success'})

    if request.user.userprofile.is_cm:
        result.update(translation.cm_urls_dict())
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['GET'])
@login_required
def take_in(request, object_id, lang_code, model):
    # model must be TranslationBase class or child
    translation = None
    result = {'response': 'error',
              'id': object_id}

    translation = get_or_create_user_translation(object_id, lang_code, model)
    if not translation:
        result.update({'error': 'Translation is busy.'})
        return HttpResponse(json.dumps(result), mimetype="application/json")

    if translation.has_perm(request.user, lang_code) and \
       translation.c_status == translation.inner_state.NONE:
        translation.take_in(request.user)
        result.update(translation.get_init_data(request.user))

        takein_notification.delay(translation, translation.is_done())
        result.update({'response': 'success'})
    else:
        result.update({'error': 'Has no permission'})
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['GET'])
@login_required
def take_off(request, object_id, lang_code, model):
    # model must be TranslationBase class or child
    translation = None
    result = {'response': 'error',
              'error': 'Translation is busy.'}
    try:
        translation = model.objects.get(
            c_status__in=[model.inner_state.TRANSLATION, model.inner_state.CORRECTION],
            owner_candidate=request.user,
            **model.get_params(object_id, lang_code))
    except model.DoesNotExist:
        result.update({'error': 'Translation record not found.'})
    else:
        takeoff_notification.delay(translation)
        translation.clear_state()
        del result['error']
        result.update({'response': 'success',
                       'take_in_url': translation.take_in_url(lang_code)})
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['POST'])
@login_required
def done(request, object_id, lang_code, model):
    # model must be TranslationBase class or child
    translation = None
    result = {'response': 'error',
              'error': 'Translation is busy.'}
    try:
        translation = model.objects.get(
            c_status__in=[model.inner_state.TRANSLATION, model.inner_state.CORRECTION],
            owner_candidate=request.user,
            **model.get_params(object_id, lang_code))
    except model.DoesNotExist:
        result.update({'error': 'Translation record not found.'})
    else:
        if translation.has_perm(request.user, lang_code) and \
           translation.c_status in [translation.inner_state.TRANSLATION,
                                    translation.inner_state.CORRECTION]:
            translation.set_done(request.POST)
            approve_notification.delay(translation)
            result.update({'response': 'success'})

        if request.user.userprofile.is_cm:
            result.update(translation.cm_urls_dict())
    return HttpResponse(json.dumps(result), mimetype="application/json")


def _approve_correct_revoke(request, object_id, lang_code, model, params):
    # model must be TranslationBase class or child
    params.update(model.get_params(object_id, lang_code))
    translation = None
    result = {'response': 'error'}
    if not request.user.userprofile.is_cm:
        result.update({'error': 'Has no permission. Only CMs are allowed.'})
    else:
        try:
            translation = model.objects.get(**params)
        except model.DoesNotExist:
            result.update({'error': 'Translation record not found.'})
    return result, translation


@require_http_methods(['POST'])
@login_required
def approve(request, object_id, lang_code, model):
    # request, object_id, lang_code, model
    # model must be TranslationBase class or child
    params = {'status__gte': TranslationBase.global_state.PENDING,
              'c_status': TranslationBase.inner_state.APPROVAL}
    result, translation = _approve_correct_revoke(request, object_id, lang_code, model, params)
    if translation:
        translation.approve(request.POST)
        approved_notification.delay(translation)
        translation.clear_state()
        result.update({'response': 'success'})
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['GET'])
@login_required
def corrections(request, object_id, lang_code, model):
    # request, object_id, lang_code, model
    # model must be TranslationBase class or child
    params = {'status__gte': TranslationBase.global_state.PENDING,
              'c_status': TranslationBase.inner_state.APPROVAL}
    result, translation = _approve_correct_revoke(request, object_id, lang_code, model, params)
    if translation:
        translation.c_status = translation.inner_state.CORRECTION
        translation.timer = datetime.now()
        translation.save()
        takein_notification.delay(translation, True)
        result.update({'response': 'success'})

    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(['GET'])
@login_required
def revoke(request, object_id, lang_code, model):
    # request, object_id, lang_code, model
    # model must be TranslationBase class or child
    params = {'status__gte': TranslationBase.global_state.PENDING,
              'c_status__gt': TranslationBase.inner_state.NONE}
    result, translation = _approve_correct_revoke(request, object_id, lang_code, model, params)
    if translation:
        revoke_notification.delay(translation)
        translation.clear_state()
        result.update({'response': 'success'})
    return HttpResponse(json.dumps(result), mimetype="application/json")
