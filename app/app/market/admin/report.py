from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from postman.models import Message
from postman.admin import MessageAdmin, MessageAdminForm as MessageAdminFormBase

import app.market.models as models


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


class IncidentChangeList(ChangeList):
    def get_results(self, request):
        super(IncidentChangeList, self).get_results(request)
        orig_queryset = self.result_list
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
        self.result_list = market_items
        return market_items


class IncidentAdmin(admin.ModelAdmin):
    list_select_related = ('messageext',)
    list_display = (
        'get_id', 'title', 'get_view_count', 'commentcount',
        'get_email_rec_count', 'get_user_rec_count', 'get_conversation_count',
        'get_total_msg_count'
    )
    actions = None

    def get_id(self, obj):
        return obj.id
    get_id.short_description = _('id')

    def get_view_count(self, obj):
        return obj.view_count
    get_view_count.short_description = _('views')

    def get_email_rec_count(self, obj):
        return obj.email_rec_count
    get_email_rec_count.short_description = _('number of email recommendations')

    def get_user_rec_count(self, obj):
        return obj.user_rec_count
    get_user_rec_count.short_description = _('number of user recommendations')

    def get_conversation_count(self, obj):
        return obj.conversation_count
    get_conversation_count.short_description = _('conversation count')

    def get_total_msg_count(self, obj):
        return obj.total_msg_count
    get_total_msg_count.short_description = _('total messages count')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def __init__(self, model, admin_site):
        self.list_display_links = (None,)
        super(IncidentAdmin, self).__init__(model, admin_site)

    def get_changelist(self, request, **kwargs):
        return IncidentChangeList

admin.site.register(models.Reporting, IncidentAdmin)


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
