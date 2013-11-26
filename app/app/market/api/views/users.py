import json

from app.market.api.utils import *
import app.market as market
from app.market.forms import item_forms,saveMarketItem
import app.users as users
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext



def getAvatar(request,obj_id, rtype):
	user = get_object_or_404(users.models.User, pk=obj_id)
	obj = user.avatar_set.all()
	if obj != []:
		return HttpResponse(value(rtype,obj),mimetype="application"+rtype)
	return HttpResponse(value(rtype, [{'pk': 0, 'avatar': '/static/images/male200.png' },]),mimetype="application"+rtype)



def getDetails(request,obj_id, rtype):
	user = get_object_or_404(users.models.User, pk=obj_id)
	return HttpResponse(
		value(rtype,
			[user],
			fields=('username',)
			 ),
		mimetype="application"+rtype)


def getUsers(request,rtype):
	pass


def getUserCount(request,rtype):
	pass
	