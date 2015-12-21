from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import NewsletterSignups, Partner, HomePageBanner
from django.utils import translation
from market.models import MarketItem, Comment, EmailRecommendation
from postman.models import Message
from users.models import User, Countries
import json
import re
import os.path


def home(request):
    if request.user.is_authenticated():
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
    view_dict = {'partners_first': partners_first, 'partners_rest': partners_rest,
                 'banner': HomePageBanner.objects.filter(enabled=True)}
    return render_to_response('ahr/home_v2.html', view_dict, context_instance=RequestContext(request))


def home_test(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('exchange'))
    view_dict = {'banner': HomePageBanner.objects.filter(enabled=True)}
    return render_to_response('ahr/home.html', view_dict, context_instance=RequestContext(request))


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


def project_shield_verification(request):
    return render_to_response('misc/google9e5bfcc08bec3049.html', {}, context_instance=RequestContext(request))


def citation(request):
    return render_to_response('marketing/citation.html', {}, context_instance=RequestContext(request))


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


def tinymce_page(request, tinymce_page_detail):
    base_page = 'admin_static/tinymce_admin/static/tiny_mce/'
    popup_list = ['tiny_mce_popup.js', 'validate.js', 'mctabs.js', 'form_utils.js']
    file_name = os.path.basename(tinymce_page_detail)
    if file_name in popup_list:
        split_path = tinymce_page_detail.split('/')
        tinymce_page_detail = '/'.join(split_path[1:])

    if file_name == 'link.js':
        tinymce_page_detail = 'themes/advanced/js/link.js'

    extension = os.path.splitext(tinymce_page_detail)[1][1:]
    content_type = None
    if extension == 'js':
        content_type = 'application/javascript'
    if extension == 'css':
        content_type = 'text/css'
    if extension == 'html' or extension == 'htm':
        content_type = 'text/html'
    if extension == 'gif' or extension == 'png':
        redirect_url = settings.STATIC_URL + 'images/v2/tinymce/' + os.path.basename(tinymce_page_detail)
        return HttpResponseRedirect(redirect_url)
    return render_to_response(base_page + tinymce_page_detail, {},
                              context_instance=RequestContext(request), content_type=content_type)