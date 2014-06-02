from django.contrib import admin
import app.market.models as models
import django.db as db


class RequestManager(db.models.Manager):
    def get_query_set(self):
        return super(RequestManager, self).get_query_set().filter(item_type='request')

class Request(models.MarketItem):
    class Meta:
        proxy = True
    objects = RequestManager()


class RequestAdmin(admin.ModelAdmin):
    exclude=('item_type',)
    list_display = ('title', 'owner', 'pub_date', 'published')
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('owner', 'pub_date', 'closed_date')
        return self.readonly_fields


admin.site.register(Request,RequestAdmin)

