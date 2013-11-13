from django.contrib.auth.decorators import permission_required
from django.db.models import Q,Max,F
from django.http import HttpResponse
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, loader
from app.api.utils import *
from app.market.forms import newofferForm,commentForm


def addOffer_form(request):
    form = newofferForm()
    return render_to_response('market/offer.html',
                              {
                                  'offer':'false',
                                  'form':form
                               },
                              context_instance=RequestContext(request))


def editOffer_form(request,obj_id):
    form = newofferForm()
    return render_to_response('market/offer.html',
                              {
                                  'offer': {'id':str(obj_id)},
                                  'form':form
                               },
                              context_instance=RequestContext(request))


def viewOffer(request,obj_id):
    #get the object , populate the form? can we do that?
    return render_to_response('market/viewsingleoffer.html',
                              {
                                'offer': {'id':str(obj_id)}
                              },
                              context_instance=RequestContext(request))


def addComment_form(request,obj_type,obj_id):
    form = commentForm()
    return render_to_response('market/commentform.html',
                              {
                                  'obj_type' : obj_type,
                                  'obj_id': str(obj_id),
                                  'form': form,
                                  'coment': 'false'
                               },
                              context_instance=RequestContext(request))


def viewComment(request,obj_id):
    pass


def editComment_form(request,obj_id):
    form = commentForm()
    return render_to_response('market/commentform.html',
                              {
                                  'obj_type' : '',
                                  'obj_id': '""',
                                  'form': form,
                                  'coment': {'id':str(obj_id)}
                               },
                              context_instance=RequestContext(request))

