from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import Http404

from app.users.models import Interest, Countries, Skills
from forms import RequestForm, OfferForm, save_market_item
from models.market import MarketItem, MarketItemViewCounter


def index(request):
    interests = Interest.objects.all()
    countries = Countries.objects.all()
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
                                  'regions': regions,
                                  'countries': countries,
                                  'is_logged_in': request.user.is_authenticated()
                              },
                              context_instance=RequestContext(request))


def show_post(request, post_id):
    post = get_object_or_404(MarketItem.objects.defer('comments'),
                             pk=post_id,
                             deleted=False,
                             owner__is_active=True)

    if post.is_closed():
        raise Http404('No post matches the given query.')

    language_list = []
    if request.user.is_authenticated():
        MarketItemViewCounter.objects.get_or_create(viewer_id=request.user.id, item_id=post_id)
        language_list = request.user.userprofile.languages.all()

    post_data = {
        'post': post,
        'report_url': reverse('report_post', args=[post.id]),
        'is_logged_in': request.user.is_authenticated(),
        'language_list': language_list,
    }

    return render_to_response('market/view_post.html', post_data, context_instance=RequestContext(request))


@login_required
def create_offer(request):
    user_skills = request.user.userprofile.interests.values_list('id', flat=True)
    user_countries = request.user.userprofile.countries.values_list('id', flat=True)
    form = OfferForm(request.POST or None, user_skills=user_skills, user_countries=user_countries)
    if form.is_valid():
        save_market_item(form, request.user)
        # TODO This needs to be the new view offer page
        return redirect('/')
    return render_to_response('market/create_offer.html', {'form': form},
                              context_instance=RequestContext(request))


@login_required
def create_request(request):
    user_skills = request.user.userprofile.interests.values_list('id', flat=True)
    user_countries = request.user.userprofile.countries.values_list('id', flat=True)
    form = RequestForm(request.POST or None, user_skills=user_skills, user_countries=user_countries)
    if form.is_valid():
        save_market_item(form, request.user)
        # TODO This needs to be the new view request page
        return redirect(reverse('request_posted'))
    return render_to_response('market/create_request.html', {'form': form},
                              context_instance=RequestContext(request))


@login_required
def request_posted(request):
    if request.POST:
        return redirect(reverse('show_market'))
    return render_to_response('market/request_posted.html', {},
                              context_instance=RequestContext(request))

@login_required
def edit_offer(request, post_id):
    market_item = get_object_or_404(MarketItem, pk=post_id)
    form = OfferForm(request.POST or None, instance=market_item)
    if form.is_valid():
        save_market_item(form, request.user)
        return redirect(reverse('home'))
    return render_to_response('market/create_offer.html', {'form': form},
                              context_instance=RequestContext(request))


@login_required
def edit_request(request, post_id):
    market_item = get_object_or_404(MarketItem, pk=post_id)
    form = RequestForm(request.POST or None, instance=market_item)
    if form.is_valid():
        save_market_item(form, request.user)
        return redirect(reverse('home'))
    return render_to_response('market/create_request.html', {'form': form},
                              context_instance=RequestContext(request))


@login_required
def notifications(request):
    return render_to_response('market/notifications.html', {},
                              context_instance=RequestContext(request))

@login_required
def permanent_delete_postman(request):
    return redirect(reverse('postman_trash'))
