from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from postman.models import Message
from postman.admin import MessageAdmin, MessageAdminForm as MessageAdminFormBase

import app.market.models as models
from ..utils import export_as_csv


class MarketItemPostReportAdmin(admin.ModelAdmin):
    list_display = ('item_owner', 'reportedby', 'pub_date', 'resolved' )
    readonly_fields = ('owner', 'item')
    def item_owner(self,obj):
        return obj.item.owner.username

    def reportedby(self,obj):
        return obj.owner.username

admin.site.register(models.MarketItemPostReport, MarketItemPostReportAdmin)

class UserReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'reportedby', 'pub_date', 'resolved' )
    readonly_fields = ('owner', 'user')    

    def reportedby(self,obj):
        return obj.owner.username

admin.site.register(models.UserReport, UserReportAdmin)

admin.site.register(models.EmailRecommendation)


def _make_incident_queryset(orig_queryset):
    queryset = orig_queryset.annotate(
        view_count=Count('marketitemviewconter', distinct=True),
        email_rec_count=Count('emailrecommendation', distinct=True),
        total_msg_count=Count('messageext', distinct=True),
    )
    user_rec_dict = dict(orig_queryset.filter(
        messageext__is_post_recommendation=True).annotate(
            user_rec_count=Count('messageext')
        ).values_list('id', 'user_rec_count'))
    conversation_dict = dict(orig_queryset.filter(
        messageext__thread=None).annotate(
            conversation_count=Count('messageext')
        ).values_list('id', 'conversation_count'))
    market_items = queryset[:]
    for item in market_items:
        item.user_rec_count = user_rec_dict.get(item.id, 0)
        item.conversation_count = conversation_dict.get(item.id, 0)
    return market_items


class IncidentChangeList(ChangeList):
    def get_results(self, request):
        super(IncidentChangeList, self).get_results(request)
        orig_queryset = self.result_list
        self.result_list = _make_incident_queryset(orig_queryset)


class ActionsInline(admin.TabularInline):
    model = models.MarketItemActions


class NextStepsInline(admin.TabularInline):
    model = models.MarketItemNextSteps


class IncidentAdmin(admin.ModelAdmin):
    list_select_related = ('messageext',)
    readonly_fields = ('closed_date',)
    list_display_links = ('id', 'title',)
    list_display = (
        'id', 'title', 'get_view_count', 'commentcount',
        'get_email_rec_count', 'get_user_rec_count', 'get_conversation_count',
        'get_total_msg_count', 'get_screen_name', 'get_create_date',
        'get_owner', 'get_aging', 'get_status'
    )
    csv_field_exclude = ('title', 'owner', 'pub_date', 'status')
    actions = None
    inlines = (ActionsInline, NextStepsInline)
    change_list_template = 'admin/incident_change_list.html'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_changelist(self, request, **kwargs):
        return IncidentChangeList

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST':
            if '_export' in request.POST:
                return export_as_csv(
                    self, _make_incident_queryset(self.get_queryset(request)))
        return super(IncidentAdmin, self).changelist_view(request,
                                                          extra_context)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'staff_owner':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super(IncidentAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

admin.site.register(models.IncidentTracking, IncidentAdmin)


# Replacement the standard postman model to the extended model.
class MessageAdminForm(MessageAdminFormBase):
    class Meta:
        model = models.MessagePresentation

MessageAdmin.form = MessageAdminForm
MessageAdmin.fieldsets = MessageAdmin.fieldsets + ((
    _('Additional properties'), {'fields': (
        ('is_post_recommendation', 'is_user_recommendation', 'market_item'),)
    }),)
admin.site.unregister(Message)
admin.site.register(models.MessagePresentation, MessageAdmin)
