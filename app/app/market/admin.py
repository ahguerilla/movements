from django.contrib import admin
import models
import django.db as db


class OfferManager(db.models.Manager):
    def get_query_set(self):
        return super(OfferManager, self).get_query_set().filter(item_type='offer')


class Offer(models.MarketItem):
    class Meta:
        proxy = True
    objects = OfferManager()


class OfferAdmin(admin.ModelAdmin):
    exclude = ('item_type',)
    list_display = ('title', 'owner', 'pub_date', 'published')
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('owner','pub_date')
        return self.readonly_fields


admin.site.register(Offer, OfferAdmin)


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
            return self.readonly_fields + ('owner','pub_date')
        return self.readonly_fields


admin.site.register(Request,RequestAdmin)


class ResourceManager(db.models.Manager):
    def get_query_set(self):
        return super(ResourceManager, self).get_query_set().filter(item_type='resource')


class Resource(models.MarketItem):
    class Meta:
        proxy = True
    objects = ResourceManager()


class fileAdmin(admin.TabularInline):
    model=models.File


class ResourceAdmin(admin.ModelAdmin):
    exclude=('item_type',)
    inlines = (fileAdmin,)
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('owner','pub_date')
        return self.readonly_fields

admin.site.register(Resource,ResourceAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('contents', 'pub_date', 'published',)
    pass


admin.site.register(models.Comment,CommentAdmin)



class MarketItemPostReportAdmin(admin.ModelAdmin):
    list_display = ('item', 'contents', 'owner','resolved' )

admin.site.register(models.MarketItemPostReport, MarketItemPostReportAdmin)