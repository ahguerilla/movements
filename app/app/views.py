from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import NewsletterSignups
import json
import re


def home(request):
    if request.user.is_authenticated() and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('exchange'))
    view_dict = {'sign_up': True}
    return render_to_response('ahr/home_v2.html', view_dict, context_instance=RequestContext(request))


def terms_and_conditions(request):
    return HttpResponseRedirect('/movements/terms-and-conditions/')


def contact_us(request):
    return HttpResponseRedirect('/movements/contact-us/')


def exchange(request):
    return HttpResponseRedirect(reverse('show_market'))


def newsletter_signup(request):
    if request.POST:
        email = request.POST.get("email", "")
        result = "success" if re.match(r"[^@]+@[^@]+\.[^@]+", email) else "failed"
        message = "Thanks for your interest in movements!!" if result == "success" else "Please enter a valid email"

        if result == "success":
            try:
                signup = NewsletterSignups()
                signup.email = email
                signup.save()
            except:
                result = "failed"
                message = "Unable to process email at this time"

        response_data = {
            'result': result,
            'message': message
        }

    else:
        response_data = {
            'result': 'failed',
            'message': 'Not a valid request'
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json")