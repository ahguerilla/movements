import datetime

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from postman.models import Message
from django.db.models import Q
from django.http import Http404

from app.users.models import Interest, UserProfile
from forms import RequestForm, OfferForm, save_market_item
from models.market import MarketItem


def get_user_tags(user):
    all_skills = []
    all_countris = []
    all_issues = []
    if hasattr(user, 'userprofile'):
        all_skills = user.userprofile.skills.all()
        all_countris = user.userprofile.countries.all()
        all_issues = user.userprofile.issues.all()

    return {'skills': [up.pk for up in all_skills],
            'countries': [up.pk for up in all_countris],
            'issues': [up.pk for up in all_issues]}


@login_required
def index(request):
    return render_to_response('market/market.html',
                              {
                                  'title': 'Exchange',
                                  'help_text_template': 'market/copy/market_help.html',
                                  'init': 'market',
                                  'tags': get_user_tags(request.user)
                              },
                              context_instance=RequestContext(request))


@login_required
def show_post(request, post_id):
    post = get_object_or_404(MarketItem.objects.defer('comments'),
                             pk=post_id,
                             closed_date=None,
                             deleted=False,
                             owner__is_active=True)

    post_data = {
        'post': post,
        'report_url': reverse('report_post', args=[post.id])
    }

    return render_to_response('market/view_post.html', post_data, context_instance=RequestContext(request))


@login_required
def create_offer(request):
    user_skills = request.user.userprofile.interests.values_list('id', flat=True)
    form = OfferForm(request.POST or None, user_skills=user_skills)
    if form.is_valid():
        save_market_item(form, request.user)
        # TODO This needs to be the new view offer page
        return redirect('/')
    return render_to_response('market/create_offer.html', {'form': form},
                              context_instance=RequestContext(request))


@login_required
def create_request(request):
    user_skills = request.user.userprofile.interests.values_list('id', flat=True)
    form = RequestForm(request.POST or None, user_skills=user_skills)
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
def users(request):
    return render_to_response('market/market.html',
                              {
                                  'title': 'Members',
                                  'help_text_template': 'market/copy/user_help.html',
                                  'init': 'users',
                                  'tags': get_user_tags(request.user)
                              },
                              context_instance=RequestContext(request))


@login_required
def posts(request):
    return render_to_response('market/market.html',
                              {
                                  'title': 'My Posts',
                                  'help_text_template': 'market/copy/myposts_help.html',
                                  'init': 'posts',
                                  'tags': get_user_tags(request.user)
                              },
                              context_instance=RequestContext(request))


@login_required
def notifications(request):
    return render_to_response('market/notifications.html',
        {},
                              context_instance=RequestContext(request))


@login_required
def permanent_delete_postman(request):
    # There is only one row for both users, deleting will delete for both users
    return redirect(reverse('postman_trash'))
    tpks = request.POST.getlist('tpks')
    pks = request.POST.getlist('pks')
    user = request.user
    if pks or tpks:
        filter = Q(pk__in=pks) | Q(thread__in=tpks)
        recipient_rows = Message.objects.as_recipient(user, filter).delete()
        sender_rows = Message.objects.as_sender(user, filter).delete()
    return redirect(reverse('postman_trash'))


def preview(request, obj_type, obj_id):
    return render_to_response('market/preview.html',
                              {
                                  'title': 'Recommendation',
                                  'help_text_template': 'market/copy/recommendation_help.html',
                                  'init': 'recommendation',
                                  'obj_type': obj_type,
                                  'obj_id': obj_id
                              },
                              context_instance=RequestContext(request))
