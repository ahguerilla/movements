from django.core import serializers

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


def value(atype,objs,**kwargs):
    return serializers.serialize(atype,objs,**kwargs)

