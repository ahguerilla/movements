from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

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


class ReportAdmin(admin.ModelAdmin):
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
        return obj.marketitemviewconter_set.count()
    get_view_count.short_description = _('views')

    def get_email_rec_count(self, obj):
        return obj.emailrecommendation_set.count()
    get_email_rec_count.short_description = _('number of email recommendations')

    def get_user_rec_count(self, obj):
        return obj.extmessage_set.filter(is_post_recommendation=True).count()
    get_user_rec_count.short_description = _('number of user recommendations')

    def get_conversation_count(self, obj):
        return obj.extmessage_set.filter(thread=None).count()
    get_conversation_count.short_description = _('conversation count')

    def get_total_msg_count(self, obj):
        return obj.extmessage_set.count()
    get_total_msg_count.short_description = _('total messages count')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def __init__(self, model, admin_site):
        self.list_display_links = (None,)
        super(ReportAdmin, self).__init__(model, admin_site)


admin.site.register(models.Reporting, ReportAdmin)


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
