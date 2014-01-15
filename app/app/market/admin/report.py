from django.contrib import admin
import app.market.models as models
import django.db as db

class MarketItemPostReportAdmin(admin.ModelAdmin):
    list_display = ('item', 'contents', 'owner','resolved' )

admin.site.register(models.MarketItemPostReport, MarketItemPostReportAdmin)
