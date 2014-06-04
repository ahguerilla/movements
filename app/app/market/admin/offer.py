from django.contrib import admin
import app.market.models as models
import django.db as db
from django.contrib.auth.models import User


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
            return self.readonly_fields + ('owner', 'pub_date', 'closed_date')
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'staff_owner':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super(OfferAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


admin.site.register(Offer, OfferAdmin)
