from django.contrib import admin
import app.market.models as models
import django.db as db


class fileAdmin(admin.TabularInline):
    model=models.File


class ResourceManager(db.models.Manager):
    def get_query_set(self):
        return super(ResourceManager, self).get_query_set().filter(item_type='resource')


class Resource(models.MarketItem):
    class Meta:
        proxy = True
    objects = ResourceManager()


class ResourceAdmin(admin.ModelAdmin):
    exclude=('item_type',)
    inlines = (fileAdmin,)
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('owner','pub_date')
        return self.readonly_fields

admin.site.register(Resource,ResourceAdmin)

