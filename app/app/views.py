from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import NewsletterSignups, Partner
from django.utils import translation
from market.models import MarketItem, Comment, EmailRecommendation
from postman.models import Message
from users.models import User, Countries
import json
import re


def home(request):
    if request.user.is_authenticated() and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('exchange'))
    partners = Partner.objects.filter(enabled=True).all()
    partner_list = []
    if partners:
        length_partners = len(partners)
        remainder_4 = length_partners % 4
        large = 0
        if remainder_4 == 3:
            large = 3
        if remainder_4 == 2:
            large = 2
        if remainder_4 == 1:
            large = 1

        small = 0
        remainder_3 = length_partners % 3
        if remainder_3 == 2:
            small = 2
        if remainder_3 == 1:
            small = 1

        xsmall = 0
        remainder_2 = length_partners % 6
        if remainder_2 == 1:
            xsmall = 1

        for i in range(length_partners):
            css_class = ''
            if length_partners - i <= large:
                if large == 3:
                    css_class += 'col-lg-4 '
                if large == 2:
                    css_class += 'col-lg-6 '
                if large == 1:
                    css_class += 'col-lg-12 '
            else:
                css_class += 'col-lg-3 '

            if length_partners - i <= small:
                if small == 2:
                    css_class += 'col-sm-6 '
                if small == 1:
                    css_class += 'col-sm-12 '
            else:
                css_class += 'col-sm-4 '

            if length_partners - i <= xsmall:
                if xsmall == 1:
                    css_class += 'col-xs-12'
            else:
                css_class += 'col-xs-6'

            partner_list.append({'title': partners[i].title, 'text': partners[i].text,
                                 'logo': partners[i].logo, 'css': css_class})

    partners_first = None
    partners_rest = None
    if partner_list:
        if len(partner_list) > 2:
            partners_first = partner_list[:2]
            partners_rest = partner_list[2:]
        else:
            partners_first = partner_list
    view_dict = {'partners_first': partners_first, 'partners_rest': partners_rest}
    return render_to_response('ahr/home_v2.html', view_dict, context_instance=RequestContext(request))


def get_stats(request):
    total_connections = MarketItem.objects.count() + Comment.objects.count() + \
                        Message.objects.count() + EmailRecommendation.objects.count()
    response_data = {
        'connections': total_connections,
        'user': User.objects.count(),
        'countries': '153',
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def success_stories(request, success_story_id):
    redirect_url = '/en/movements/about-movements/success-stories/#ss' + str(success_story_id)
    return HttpResponseRedirect(redirect_url)


def youtube_verification(request):
    return render_to_response('google73f6a199341a73ff.html')


def terms_and_conditions(request):
    return HttpResponseRedirect('/movements/terms-and-conditions/')


def set_language(request):
    lang_code = request.POST.get('language_code')
    result = 'error'
    if lang_code:
        translation.activate(lang_code)
        request.LANGUAGE_CODE = translation.get_language()
        result = 'success'
    response_data = {
        'result': result,
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


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


def admin_login(request):
    raise Http404