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
