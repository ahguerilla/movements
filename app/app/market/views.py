import json

from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import Http404, HttpResponse
from app.market.api.utils import HttpResponseForbiden

from app.users.models import Interest, Countries, Issues
from app.utils import form_errors_as_dict
from forms import RequestForm, OfferForm, save_market_item
from models.market import MarketItem, MarketItemViewCounter, MarketItemSalesforceRecord, MarketItemImage


def index(request):
    interests = Interest.objects.all()
    issues = Issues.objects.all()
    countries = Countries.objects.select_related('region').all()
    region_dict = {}
    for country in countries:
        if country.region:
            region = country.region
            if region.id in region_dict:
                region_dict[region.id].country_list.append(country)
            else:
                region_dict[region.id] = region
                region.country_list = [country]
    regions = region_dict.values()
    regions = sorted(regions, key=lambda r: r.name)
    return render_to_response('market/market.html',
                              {
                                  'interests': serializers.serialize('json', interests),
                                  'issues': serializers.serialize('json', issues),
                                  'regions': regions,
                                  'countries': countries,
                                  'is_logged_in': request.user.is_authenticated()
                              },
                              context_instance=RequestContext(request))


def show_post(request, post_id):
    prefetch_list = ['interests', 'issues', 'countries', 'marketitemimage_set', 'marketitemhowcanyouhelp_set', ]
    post = get_object_or_404(MarketItem.objects.defer('comments').prefetch_related(*prefetch_list),
                             pk=post_id,
                             deleted=False,
                             owner__is_active=True)

    if post.is_closed():
        raise Http404('No post matches the given query.')

    countries_to_render = []

    countries = Countries.objects.exclude(region=None).select_related('region').all()
    by_region = defaultdict(list)
    for country in countries:
        by_region[country.region_id].append(country)

    post_countries = post.countries.all()

    if len(post_countries) == len(countries):
        countries_to_render.append('Global')
    else:
        post_countries_by_region = defaultdict(list)
        for country in post_countries:
            post_countries_by_region[country.region_id].append(country)
        for region_id in post_countries_by_region:
            post_region_countries = post_countries_by_region[region_id]
            region_countries = by_region[region_id]
            if len(post_region_countries) == len(region_countries):
                countries_to_render.append(region_countries[0].region.name)
            else:
                for country in post_region_countries:
                    countries_to_render.append(country)
    language_list = []
    translation_languages = []
    translator = False
    if request.user.is_authenticated():
        __, created = MarketItemViewCounter.objects.get_or_create(viewer_id=request.user.id, item_id=post_id)
        if created:
            MarketItemSalesforceRecord.mark_for_update(post_id)
        language_list = request.user.userprofile.languages.all()
        translation_languages = list(request.user.userprofile.translation_languages.all())
    if len(translation_languages) > 1:
        for l in translation_languages:
            if l.language_code == post.language:
                translator = True
                break
    if not translator:
        translation_languages = []

    post_data = {
        'post': post,
        'images': post.marketitemimage_set.all(),
        'report_url': reverse('report_post', args=[post.id]),
        'is_logged_in': request.user.is_authenticated(),
        'language_list': language_list,
        'countries_to_render': countries_to_render,
        'translator': translator,
        'translation_languages': json.dumps([{'code': l.language_code, 'name': l.name} for l in translation_languages]),
    }

    return render_to_response('market/view_post.html', post_data, context_instance=RequestContext(request))


def _create_or_update_post(request, template, form_class, build_redir_url, market_item):
    if market_item:
        form = form_class(request.POST or None, instance=market_item)
    else:
        user_skills = request.user.userprofile.interests.values_list('id', flat=True)
        user_countries = request.user.userprofile.countries.values_list('id', flat=True)
        form = form_class(request.POST or None, user_skills=user_skills, user_countries=user_countries)
    if form.is_valid():
        post = save_market_item(form, request.user)
        if market_item:
            del_ids = []
            for item in request.POST:
                if item.startswith('delete_image_'):
                    img_id = int(item.replace('delete_image_', ''))
                    del_ids.append(img_id)
            MarketItemImage.objects.filter(item=market_item, id__in=del_ids).delete()
        for image in request.FILES:
            MarketItemImage.save_image(post, request.FILES[image])
        redir_url = build_redir_url(post)
        if request.is_ajax():
            return HttpResponse(json.dumps({'success': True, 'redir_url': redir_url}), mimetype="application/json")
        return redirect(redir_url)
    if request.is_ajax():
        errors = form_errors_as_dict(form)
        return HttpResponse(json.dumps({'success': False, 'errors': errors}), mimetype="application/json")
    ctx = {
        'form': form,
        'images': None,
    }
    if market_item:
        ctx['images'] = market_item.marketitemimage_set.all()
    return render_to_response(template, ctx, context_instance=RequestContext(request))


@login_required
def create_offer(request):
    return _create_or_update_post(request,
                                  'market/create_offer.html',
                                  OfferForm,
                                  lambda x: reverse('show_post', args=[x.id]),
                                  None)


@login_required
def create_request(request):
    return _create_or_update_post(request,
                                  'market/create_request.html',
                                  RequestForm,
                                  lambda x: reverse('request_posted'),
                                  None)


@login_required
def request_posted(request):
    if request.POST:
        return redirect(reverse('show_market'))
    return render_to_response('market/request_posted.html', {},
                              context_instance=RequestContext(request))


@login_required
def edit_post(request, post_id):
    market_item = get_object_or_404(MarketItem.objects.defer('comments').prefetch_related('marketitemimage_set'),
                                    pk=post_id)
    if market_item.owner != request.user:
        return HttpResponseForbiden()
    if market_item.item_type == MarketItem.TYPE_CHOICES.OFFER:
        form_class = OfferForm
        tpl = 'market/create_offer.html'
    else:
        form_class = RequestForm
        tpl = 'market/create_request.html'
    return _create_or_update_post(request,
                                  tpl,
                                  form_class,
                                  lambda x: reverse('show_post', args=[x.id]),
                                  market_item)


@login_required
def notifications(request):
    return render_to_response('market/notifications.html', {},
                              context_instance=RequestContext(request))


@login_required
def permanent_delete_postman(request):
    return redirect(reverse('postman_trash'))


@login_required
def translations(request):
    if not request.user.userprofile.is_translator:
        return redirect(reverse('home'))
    translation_languages = list(request.user.userprofile.translation_languages.all())
    ctx = {
        'translation_languages': json.dumps([{'code': l.language_code, 'name': l.name} for l in translation_languages]),
    }
    return render_to_response('market/translations.html', ctx, context_instance=RequestContext(request))
