from django.contrib import admin
import app.market.models as models
import django.db as db

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
