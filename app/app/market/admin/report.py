import csv

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.http import HttpResponse

from postman.models import Message, now
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


class IncidentChangeList(ChangeList):
    def get_results(self, request):
        super(IncidentChangeList, self).get_results(request)
        orig_queryset = self.result_list
        self.result_list = self.model_admin.make_incident_queryset(
            orig_queryset)


class ActionsInline(admin.TabularInline):
    model = models.MarketItemActions


class NextStepsInline(admin.TabularInline):
    model = models.MarketItemNextSteps


class IncidentAdmin(admin.ModelAdmin):
    list_select_related = ('messageext',)
    readonly_fields = ('closed_date',)
    list_display_links = ('id', 'title',)
    list_display = (
        'id', 'title', 'get_view_count', 'commentcount',
        'get_email_rec_count', 'get_user_rec_count', 'get_conversation_count',
        'get_total_msg_count', 'get_screen_name', 'get_create_date',
        'get_owner', 'get_aging', 'get_status'
    )
    # Prevents duplicates.
    csv_field_exclude = ('owner', 'pub_date', 'status')
    actions = None
    inlines = (ActionsInline, NextStepsInline)
    change_list_template = 'admin/incident_change_list.html'
    change_form_template = 'admin/incident_change_form.html'

    # Prepare fields for change list and CSV.

    def get_view_count(self, obj):
        return obj.view_count
    get_view_count.short_description = _('views')

    def get_email_rec_count(self, obj):
        return obj.email_rec_count
    get_email_rec_count.short_description = _('number of email recommendations')

    def get_user_rec_count(self, obj):
        return obj.user_rec_count
    get_user_rec_count.short_description = _('number of user recommendations')

    def get_conversation_count(self, obj):
        return obj.conversation_count
    get_conversation_count.short_description = _('conversation count')

    def get_total_msg_count(self, obj):
        return obj.total_msg_count
    get_total_msg_count.short_description = _('total messages count')

    def get_screen_name(self, obj):
        return obj.owner
    get_screen_name.short_description = _('Screen name')

    def get_create_date(self, obj):
        return obj.pub_date
    get_create_date.short_description = _('date of post')

    def get_owner(self, obj):
        return obj.staff_owner
    get_owner.short_description = _('owner')

    def get_aging(self, obj):
        if obj.status == obj.STATUS_CHOICES.CLOSED_BY_ADMIN or \
                obj.status == obj.STATUS_CHOICES.CLOSED_BY_USER:
            return 'N/A'
        else:
            return now() - obj.pub_date
    get_aging.short_description = _('Aging')

    def get_status(self, obj):
        return obj.get_status_display()
    get_status.short_description = _('status')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_changelist(self, request, **kwargs):
        return IncidentChangeList

    # Overridden methods.

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST':
            if '_export' in request.POST:
                return self.export_as_csv(request)
        return super(IncidentAdmin, self).changelist_view(request,
                                                          extra_context)

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        if obj:
            context.update({
                'owner': obj.owner,
                'staff_owner': obj.staff_owner,
                'commenters': User.objects.filter(comment__item=obj).distinct(),
                'senders': User.objects.filter(
                    sent_messages__messageext__market_item=obj).distinct()
            })
        return super(IncidentAdmin, self).render_change_form(request, context,
                                                             add, change,
                                                             form_url, obj)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'staff_owner':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super(IncidentAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    # Utils.

    @staticmethod
    def make_incident_queryset(orig_queryset):
        queryset = orig_queryset.annotate(
            view_count=Count('marketitemviewconter', distinct=True),
            email_rec_count=Count('emailrecommendation', distinct=True),
            total_msg_count=Count('messageext', distinct=True),
        )
        user_rec_dict = dict(orig_queryset.filter(
            messageext__is_post_recommendation=True).annotate(
                user_rec_count=Count('messageext')
            ).values_list('id', 'user_rec_count'))
        conversation_dict = dict(orig_queryset.filter(
            messageext__thread=None).annotate(
                conversation_count=Count('messageext')
            ).values_list('id', 'conversation_count'))
        market_items = queryset[:]
        for item in market_items:
            item.user_rec_count = user_rec_dict.get(item.id, 0)
            item.conversation_count = conversation_dict.get(item.id, 0)
        return market_items

    def _prep_field(self, obj, field):
        """
        Returns the field as a unicode string. If the field is a callable,
        it attempts to call it first.
        """
        attr = getattr(self, field, None)
        if attr:
            attr = attr(obj)
        else:
            attr = getattr(obj, field)
        return unicode(attr).encode('utf-8')

    def export_as_csv(self, request, header=True):
        opts = self.model._meta
        field_names = [f.name for f in opts.fields]
        field_names = list(self.list_display) + field_names
        # Make unique sequence with ordering.
        unique = set()
        unique_add = unique.add
        field_names = [x for x in field_names
                       if x not in unique and not unique_add(x)]

        if self.csv_field_exclude:
            field_names = [f for f in field_names
                           if not f in self.csv_field_exclude]

        def _get_model_attr():
            return getattr(self.model, label)

        labels = [
            getattr(getattr(self, label, _get_model_attr),
                    'short_description', label) for label in field_names]

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
            unicode(opts).replace('.', '_')
        )

        writer = csv.writer(response, delimiter=';')

        if header:
            writer.writerow([unicode(label).capitalize() for label in labels])

        queryset = self.make_incident_queryset(self.get_queryset(request))
        for obj in queryset:
            writer.writerow([self._prep_field(obj, field)
                             for field in field_names])
        return response

admin.site.register(models.IncidentTracking, IncidentAdmin)


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
