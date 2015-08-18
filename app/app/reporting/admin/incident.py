# -*- coding: utf-8 -*-
import ast

from django.contrib import admin
from django.db.models import Count
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from ...market.models import MarketItemActions, MarketItemNextSteps, MarketItemSalesforceRecord
from ..models import IncidentTracking
from .base import TrackingAdmin


class ActionsInline(admin.TabularInline):
    model = MarketItemActions


class NextStepsInline(admin.TabularInline):
    model = MarketItemNextSteps


class IncidentAdmin(TrackingAdmin):
    list_select_related = ('messageext',)
    readonly_fields = (
        'closed_date', 'title', 'details', 'pub_date',
        'commentcount', 'ratecount', 'reportcount', 'score', 'tweet_permission')
    exclude = ('countries', 'issues', 'skills', 'published', 'deleted')
    list_display_links = ('id', 'title',)
    list_display = (
        'id', 'title', 'commentcount', 'get_view_count',
        'get_email_rec_count', #'get_conversation_count', 'get_user_rec_count',
        'get_total_msg_count', 'get_screen_name', 'get_create_date',
        'get_owner', 'get_aging', 'get_status', 'is_featured', 'tweet_permission'
    )
    list_filter = ('status', 'issues')
    # Prevents duplicates.
    csv_field_exclude = ('owner', 'pub_date', 'status')
    actions = None
    inlines = (ActionsInline, NextStepsInline)
    change_list_template = 'admin/incident_change_list.html'
    change_form_template = 'admin/incident_change_form.html'

    def get_email_rec_count(self, obj):
        return obj.email_rec_count
    get_email_rec_count.short_description = _('number of email recommendations')

    # def get_user_rec_count(self, obj):
    #     return obj.user_rec_count
    # get_user_rec_count.short_description = _('number of user recommendations')

    # def get_conversation_count(self, obj):
    #     return obj.conversation_count
    # get_conversation_count.short_description = _('conversation count')

    def get_view_count(self, obj):
        return obj.total_view_count
    get_view_count.short_description = _('number of views')

    def get_total_msg_count(self, obj):
        return obj.total_msg_count
    get_total_msg_count.short_description = _('total messages count')

    def get_screen_name(self, obj):
        return obj.owner
    get_screen_name.short_description = _('Screen name')
    get_screen_name.admin_order_field = 'owner'

    def get_create_date(self, obj):
        return obj.pub_date
    get_create_date.short_description = _('date of post')
    get_create_date.admin_order_field = 'pub_date'

    def get_owner(self, obj):
        return obj.staff_owner
    get_owner.short_description = _('owner')
    get_owner.admin_order_field = 'staff_owner'

    def get_aging(self, obj):
        if obj.status == obj.STATUS_CHOICES.CLOSED_BY_ADMIN or \
                obj.status == obj.STATUS_CHOICES.CLOSED_BY_USER:
            return 'N/A'
        else:
            return now() - obj.pub_date
    get_aging.short_description = _('Aging')
    get_aging.admin_order_field = 'pub_date'

    def get_status(self, obj):
        return obj.get_status_display()
    get_status.short_description = _('status')
    get_status.admin_order_field = 'status'

    # Overridden methods.
    def save_model(self, request, obj, form, change):
        obj.save()
        MarketItemSalesforceRecord.mark_for_update(obj.id)

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        if obj:
            context.update({
                'owner': obj.owner,
                'staff_owner': obj.staff_owner,
                'commenters': self.user_model.objects.filter(
                    comment__item=obj).distinct(),
                'senders': self.user_model.objects.filter(
                    sent_messages__messageext__market_item=obj).distinct(),
                'feedback': ast.literal_eval(obj.feedback_response or '[]')
            })
        return super(IncidentAdmin, self).render_change_form(request, context,
                                                             add, change,
                                                             form_url, obj)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'staff_owner':
            kwargs['queryset'] = self.user_model.objects.filter(is_staff=True)
        return super(IncidentAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    # Utils.

    @staticmethod
    def make_tracking_queryset(orig_queryset):
        queryset = orig_queryset.annotate(
            email_rec_count=Count('emailrecommendation', distinct=True),
            total_msg_count=Count('messageext', distinct=True),
            total_view_count=Count('marketitemviewcounter', distinct=True),
        )
        # user_rec_dict = dict(orig_queryset.filter(
        #     messageext__is_post_recommendation=True).annotate(
        #         user_rec_count=Count('messageext')
        #     ).values_list('id', 'user_rec_count'))
        # conversation_dict = dict(orig_queryset.filter(
        #     messageext__parent=None).annotate(
        #         conversation_count=Count('messageext')
        #     ).values_list('id', 'conversation_count'))
        market_items = queryset[:]
        #for item in market_items:
            #item.user_rec_count = user_rec_dict.get(item.id, 0)
            #item.conversation_count = conversation_dict.get(item.id, 0)
        return market_items

admin.site.register(IncidentTracking, IncidentAdmin)
