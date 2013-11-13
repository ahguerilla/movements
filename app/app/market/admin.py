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
    pass

admin.site.register(Offer, OfferAdmin)


class RequestManager(db.models.Manager):
    def get_query_set(self):
        return super(RequestManager, self).get_query_set().filter(item_type='request')

class Request(models.MarketItem):
    class Meta:
        proxy = True
    objects = RequestManager()


class RequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(Request,RequestAdmin)


class ResourceManager(db.models.Manager):
    def get_query_set(self):
        return super(ResourceManager, self).get_query_set().filter(item_type='request')


class Resource(models.MarketItem):
    class Meta:
        proxy = True
    objects = ResourceManager()


class ResourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Resource,ResourceAdmin)


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Comment,CommentAdmin)
