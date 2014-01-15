from django.core import serializers
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


class HttpResponseError(HttpResponse):
    status_code=500

class HttpResponseForbiden(HttpResponse):
    status_code=403



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_validation_errors(form):
    return { 'success' : False,
             'errors' : [(k, form.error_class.as_text(v)) for k, v in form.errors.items()] }


def get_val_errors(form):
    errors = []
    for k, v in form.errors.items():
        errors.append({
            'field': k,
            'errors': [i for i in v]
        })

    return { 'success' : False,
             'errors' : errors }


def value(atype,objs,**kwargs):
    return serializers.serialize(atype,objs,**kwargs)

def check_perms_and_get(object_class):
    def __decorator(view_func):
        def _decorator(request, *args, **kwargs):
            obj = get_object_or_404(object_class.objects,pk=kwargs['obj_id'])
            if request.user != obj.owner:
                request.obj = None
                return HttpResponseForbiden()
            request.obj=obj
            response = view_func(request, *args, **kwargs)
            return response
        return wraps(view_func)(_decorator)
    return __decorator