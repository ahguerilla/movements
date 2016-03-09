from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.functional import curry
import django.db as db

import bleach


import app.market.models as models
from app.market.tasks.translations import mark_translations_for_update


class PostManager(db.models.Manager):
    def __init__(self, request_type):
        super(PostManager, self).__init__()
        self.request_type = request_type

    def get_query_set(self):
        return super(PostManager, self).get_query_set().filter(item_type=self.request_type)


class Request(models.MarketItem):
    class Meta:
        proxy = True
    objects = PostManager('request')


class Offer(models.MarketItem):
    class Meta:
        proxy = True
    objects = PostManager('offer')


class News(models.MarketItem):
    class Meta:
        proxy = True
        verbose_name_plural = 'news'
    objects = PostManager('news')


class MarketItemHowCanYouHelpInline(admin.TabularInline):
    model = models.MarketItemHowCanYouHelp
    extra = 1


class MarketItemImageInline(admin.TabularInline):
    model = models.MarketItemImage
    exclude = ('original_metadata',)
    extra = 0


class MarketItemRelatedPostInline(admin.TabularInline):
    model = models.MarketItemRelatedPost
    fk_name = 'market_item'
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        if request.method == "GET":
            initial.append({
                'creator': request.user,
            })
        formset = super(MarketItemRelatedPostInline, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        return formset


class PostAdmin(admin.ModelAdmin):
    exclude = ('item_type',)
    list_display = ('title', 'owner', 'staff_owner', 'pub_date', 'published')
    inlines = (MarketItemImageInline, MarketItemHowCanYouHelpInline, )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('owner', 'closed_date')
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'staff_owner':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super(PostAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.save()
        mark_translations_for_update(obj)
        models.MarketItemSalesforceRecord.mark_for_update(obj.id)

    def save_formset(self, request, form, formset, change):
        if formset.model == models.MarketItemHowCanYouHelp:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.text = bleach.clean(instance.text,
                                             tags=['a', 'img', 'bold', 'strong', 'i', 'em'],
                                             attributes=['href', 'title', 'alt', 'src'], strip=True)
                instance.save()
            formset.save_m2m()
            return instances
        return formset.save()


class NewsAdmin(PostAdmin):
    inlines = (MarketItemRelatedPostInline, MarketItemImageInline, MarketItemHowCanYouHelpInline, )


admin.site.register(Offer, PostAdmin)
admin.site.register(Request, PostAdmin)
admin.site.register(News, NewsAdmin)
