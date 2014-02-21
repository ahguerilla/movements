from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from app.market.api.utils import get_val_errors
import json
import app.market as market
from app.market.forms import reportMarketItemForm, reportUserForm
from django.core.mail import send_mail
import constance
import django.contrib.auth as auth



def create_marketitem_json(item):
    return {
        'pub_date': str(item.pub_date),
        'contents': item.contents,
    }


@login_required
def report_marketitem(request, obj_id, rtype):
    if request.method == "POST":
        market_item = get_object_or_404(market.models.MarketItem.objects.only('pk'), pk=obj_id)
        if request.is_ajax():
            form = reportMarketItemForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.owner = request.user
                f.item = market_item
                f.save_base()
                send_mail('User '+request.user.username+' reported the '+market_item.item_type+' "'+ market_item.title +'" by '+ market_item.owner.username,
                          f.contents,
                          constance.config.NO_REPLY_EMAIL,[constance.config.REPORT_POST_EMAIL],
                          fail_silently=False)
                return HttpResponse(json.dumps({'success': True, 'data': create_marketitem_json(f)}), mimetype="application"+rtype)
            else:
                return HttpResponseBadRequest(json.dumps(get_val_errors(form)), mimetype="application"+rtype)

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
                send_mail('User '+request.user.username+' reported user '+user.username+' "',
                          f.contents+'\r\n to view this user in admin :'+
                          ''+
                          'to view this user profile click: '+
                          ''
                          ,
                          constance.config.NO_REPLY_EMAIL,[constance.config.REPORT_POST_EMAIL],
                          fail_silently=False)
                return HttpResponse(json.dumps({'success': True, 'data': create_marketitem_json(f)}), mimetype="application"+rtype)
            else:
                return HttpResponseBadRequest(json.dumps(get_val_errors(form)), mimetype="application"+rtype)

    return HttpResponseNotAllowed('Invalid request')
