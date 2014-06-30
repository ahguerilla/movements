from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from app.users.models import Interest, Countries
from forms import RequestForm, OfferForm, save_market_item
from models.market import MarketItem


@login_required
def index(request):
    interests = Interest.objects.all()
    countries = Countries.objects.all()
    region_dict = {}
    for country in countries:
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
                                  'title': 'Exchange',
                                  'help_text_template': 'market/copy/market_help.html',
                                  'interests': serializers.serialize('json', interests),
                                  'regions': regions,

                              },
                              context_instance=RequestContext(request))


def show_post(request, post_id):
    post = get_object_or_404(MarketItem.objects.defer('comments'),
                             pk=post_id,
                             closed_date=None,
                             deleted=False,
                             owner__is_active=True)

    post_data = {
        'post': post,
        'report_url': reverse('report_post', args=[post.id]),
        'is_logged_in': request.user.is_authenticated() and request.user.has_full_access(),
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
        return redirect('/')
    return render_to_response('market/create_request.html', {'form': form},
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
    return render_to_response('market/notifications.html',
        {},
                              context_instance=RequestContext(request))


@login_required
def permanent_delete_postman(request):
    return redirect(reverse('postman_trash'))
