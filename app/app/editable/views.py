from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from models import Placeholder, EditForm

def admin_edit(request, location_name, template_name="admin-edit.html"):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')

    try:
        placeholder = Placeholder.objects.get(location=location_name)
    except Placeholder.DoesNotExist:
        raise Http404

    if request.POST:
        placeholder_data = request.POST.copy()
        placeholder_form = EditForm(data=placeholder_data, instance=placeholder)

        if placeholder_form.is_valid():
            placeholder_form.save()
            return HttpResponseRedirect(placeholder_form.data['redirectaddr'])

    else:
        initi =[('redirectaddr',request.environ['HTTP_REFERER']) if request.environ.has_key('HTTP_REFERER') else ('redirectaddr',request.GET['redirectaddr']),]
        placeholder_form = EditForm(initial=initi,instance=placeholder)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

