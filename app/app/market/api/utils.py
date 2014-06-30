from django.core import serializers
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from postman.api import _get_site
from postman.models import Message, STATUS_ACCEPTED


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


def pm_write(sender, recipient, subject, body='', skip_notification=False,
             auto_archive=False, auto_delete=False, auto_moderators=None):
    """
    Based on the postman API.
    Write a message to a User.
    Optional arguments:
        ``skip_notification``: if the normal notification event is not wished
        ``auto_archive``: to mark the message as archived on the sender side
        ``auto_delete``: to mark the message as deleted on the sender side
        ``auto_moderators``: a list of auto-moderation functions
    """
    message = Message(
        subject=subject, body=body, sender=sender, recipient=recipient)
    initial_status = message.moderation_status
    if auto_moderators:
        message.auto_moderate(auto_moderators)
    else:
        message.moderation_status = STATUS_ACCEPTED
    message.clean_moderation(initial_status)
    if auto_archive:
        message.sender_archived = True
    if auto_delete:
        message.sender_deleted_at = now()
    message.save()
    if not skip_notification:
        message.notify_users(initial_status, _get_site())
    return message
