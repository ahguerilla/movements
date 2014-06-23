from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from app.market.api.utils import get_val_errors
import json
import app.market as market
from django.core.urlresolvers import reverse
from app.market.forms import ReportMarketItemForm, reportUserForm
from django.core.mail import send_mail, EmailMessage
import constance
import django.contrib.auth as auth
from django.contrib.sites.models import get_current_site
from django.template.loader import render_to_string


def create_marketitem_json(item):
    return {
        'pub_date': str(item.pub_date),
        'contents': item.contents,
    }


@login_required
def report_marketitem(request, obj_id):
    if request.method == "POST":
        market_item = get_object_or_404(market.models.MarketItem.objects.only('pk'), pk=obj_id)
        form = ReportMarketItemForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest(json.dumps(get_val_errors(form)), mimetype="application" + rtype)
        f = form.save(commit=False)
        f.owner = request.user
        f.item = market_item
        f.save_base()
        site = get_current_site(request)
        subj_cntxt = {
            'user': request.user.username,
            'item_type': market_item.item_type,
            'item_title': market_item.title,
            'item_owner': market_item.owner.username
        }
        subject = render_to_string('emails/itemreport_subject.html', subj_cntxt)

        text_cntxt = {
            'contents': f.contents,
            'link': site.domain + reverse('show_market') + '#item/' + str(market_item.id),
        }
        text = render_to_string('emails/itemreport.html', text_cntxt)

        email = EmailMessage(
            subject,
            text,
            constance.config.NO_REPLY_EMAIL,[constance.config.REPORT_POST_EMAIL]
        )
        email.content_subtype = "html"
        email.send()
        return HttpResponse(json.dumps({'success': True, 'data': create_marketitem_json(f)}), mimetype="application/json")
    return HttpResponseNotAllowed('Invalid request')



@login_required
def report_user(request, username, rtype):
    if request.method == "POST":
        user = get_object_or_404(auth.models.User.objects.only('username'), username=username)
        if request.is_ajax():
            form = reportUserForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.owner = request.user
                f.user = user
                f.save_base()
                site = get_current_site(request)

                subj_cntxt = {
                    'user': request.user.username,
                    'another_user': user.username
                }
                subject = render_to_string('emails/userreport_subject.html', subj_cntxt)

                text_cntxt = {
                    'contents': f.contents,
                    'link': site.domain + '/admin/auth/user/' + str(user.id)
                }
                text = render_to_string('emails/userreport.html', text_cntxt)

                email = EmailMessage(
                    subject,
                    text,
                    constance.config.NO_REPLY_EMAIL,
                    [constance.config.REPORT_POST_EMAIL]
                )
                email.content_subtype = "html"
                email.send()
                return HttpResponse(json.dumps({'success': True, 'data': create_marketitem_json(f)}), mimetype="application"+rtype)
            else:
                return HttpResponseBadRequest(json.dumps(get_val_errors(form)), mimetype="application"+rtype)

    return HttpResponseNotAllowed('Invalid request')
