from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from .models import NewsletterSignups, Partner, HomePageBanner, SuccessStories
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
    view_dict = {'banner': HomePageBanner.objects.filter(enabled=True)}
    return render_to_response('ahr/home.html', view_dict, context_instance=RequestContext(request))


def creating_requests(request):
    return render_to_response('ahr/creating_requests.html', {},
                              context_instance=RequestContext(request))


def creating_offers(request):
    return render_to_response('ahr/creating_offers.html', {},
                              context_instance=RequestContext(request))


def get_stats(request):
    total_connections = MarketItem.objects.count() + Comment.objects.count() + \
                        Message.objects.count() + EmailRecommendation.objects.count()
    response_data = {
        'connections': total_connections,
        'user': User.objects.count(),
        'countries': '153',
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def success_story_item(request, success_story_id):
    ss = get_object_or_404(SuccessStories, pk=success_story_id)
    return render_to_response('ahr/success_story.html', {'success_story': ss},
                              context_instance=RequestContext(request))


def success_story_item_next(request, success_story_id):
    ss = SuccessStories.objects.filter(id__gt=success_story_id).order_by('id').first()
    if not ss:
        ss = SuccessStories.objects.order_by('id').first()
    return HttpResponseRedirect(reverse('success_story_item', args=[ss.id]))


def success_story_item_prev(request, success_story_id):

    ss = SuccessStories.objects.filter(id__lt=success_story_id).order_by('-id').first()
    if not ss:
        ss = SuccessStories.objects.order_by('-id').first()
    return HttpResponseRedirect(reverse('success_story_item', args=[ss.id]))


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