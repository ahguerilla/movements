from django.core import serializers
from django.conf import settings
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from postman.models import Message, STATUS_ACCEPTED
from tasks.celerytasks import new_postman_message
import requests
import json
from django.utils.html import strip_tags



class HttpResponseError(HttpResponse):
    status_code = 500


class HttpResponseForbiden(HttpResponse):
    status_code = 403


def get_validation_errors(form):
    return {'success': False,
            'errors': [(k, form.error_class.as_text(v)) for k, v in form.errors.items()]}


def get_val_errors(form):
    errors = []
    for k, v in form.errors.items():
        errors.append({
            'field': k,
            'errors': [i for i in v]
        })

    return {'success': False,
            'errors': errors}


def value(atype, objs, **kwargs):
    return serializers.serialize(atype, objs, **kwargs)


def check_perms_and_get(object_class):
    def __decorator(view_func):
        def _decorator(request, *args, **kwargs):
            obj = get_object_or_404(object_class.objects, pk=kwargs['obj_id'], deleted=False, owner__is_active=True)
            if request.user != obj.owner:
                request.obj = None
                return HttpResponseForbiden()
            request.obj = obj
            response = view_func(request, *args, **kwargs)
            return response

        return wraps(view_func)(_decorator)

    return __decorator


def pm_write(sender, recipient, subject, body=''):
    message = Message(
        subject=subject, body=body, sender=sender, recipient=recipient)
    initial_status = message.moderation_status
    message.moderation_status = STATUS_ACCEPTED
    message.clean_moderation(initial_status)
    message.save()
    new_postman_message.delay(message)
    return message


def translate_text(original_text, language):
    success = False
    translation = ""
    try:
        api_key = settings.GOOGLE_TRANSLATE_API_KEY
        base_url = settings.GOOGLE_TRANSLATE_BASE
        key = "key=" + api_key
        query = "q=" + strip_tags(original_text)
        target = "target=" + language
        query_string = base_url + key + "&" + query + "&" + target
        r = requests.get(query_string)
        if r.status_code == 200:
            data = json.loads(r.content)
            data = data.get("data", {}).get("translations", [])
            if len(data) > 0:
                translation = data[0].get("translatedText", "")
                if translation:
                    success = True
    except:
        pass

    return success, translation