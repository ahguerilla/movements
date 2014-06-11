# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db.models import Count
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from ...market.models import MarketItemActions, MarketItemNextSteps
from ..models import IncidentTracking, UserTracking
from .base import TrackingAdmin


class ActionsInline(admin.TabularInline):
    model = MarketItemActions


class NextStepsInline(admin.TabularInline):
    model = MarketItemNextSteps


class IncidentAdmin(TrackingAdmin):
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

    # Overridden methods.

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        if obj:
            context.update({
                'owner': obj.owner,
                'staff_owner': obj.staff_owner,
                'commenters': self.user_model.objects.filter(
                    comment__item=obj).distinct(),
                'senders': self.user_model.objects.filter(
                    sent_messages__messageext__market_item=obj).distinct()
            })
        return super(IncidentAdmin, self).render_change_form(request, context,
                                                             add, change,
                                                             form_url, obj)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'staff_owner':
            kwargs['queryset'] = self.user_model.objects.filter(is_staff=True)
        return super(IncidentAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    # Utils.

    @staticmethod
    def make_tracking_queryset(orig_queryset):
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

admin.site.register(IncidentTracking, IncidentAdmin)


class UserAdmin(TrackingAdmin):
    list_select_related = ('userprofile',)
    list_display_links = ('id', 'get_screen_name')
    list_display = (
        'id', 'get_screen_name', 'get_signup_date', 'get_full_name',
        'get_nationality', 'get_resident_country', 'email',
        'get_request_count', 'get_offer_count', 'get_comment_count',
        'last_login', 'is_admin'
    )
    change_list_template = 'admin/user_tracking_change_list.html'
    change_form_template = 'admin/user_tracking_change_form.html'
    csv_field_exclude = (
        'is_superuser', 'password', 'username', 'is_staff', 'fullname',
        'is_active', 'first_name', 'last_name')
    csv_safe_fields = csv_field_exclude + (
        'get_full_name', 'email')

    # Prepare fields for change list and CSV.

    def get_screen_name(self, obj):
        return obj.username
    get_screen_name.short_description = _('Screen Name')

    def get_signup_date(self, obj):
        return obj.date_joined
    get_signup_date.short_description = _('Signup Date')

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = _('Full Name')

    def get_nationality(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.nationality
        return ''
    get_nationality.short_description = _('Nationality')

    def get_resident_country(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.resident_country
        return ''
    get_resident_country.short_description = _('Country of Residence')

    def is_admin(self, obj):
        return obj.is_staff
    is_admin.short_description = _('Is Admin')

    def get_request_count(self, obj):
        return obj.request_count
    get_request_count.short_description = _('Request Count')

    def get_offer_count(self, obj):
        return obj.offer_count
    get_offer_count.short_description = _('Offer Count')

    def get_comment_count(self, obj):
        return obj.comment_count
    get_comment_count.short_description = _('Comment Count')

    # Overridden methods.

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST' and '_safe_export' in request.POST:
                return self.export_as_csv(request, safe_mode=True)
        return super(UserAdmin, self).changelist_view(request, extra_context)

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        if obj:
            users = self.make_tracking_queryset(
                self.get_queryset(request).filter(id=obj.id))
            obj = users[0]
            context.update(
                {'report_fields': [
                    (label, self._prep_field(obj, field))
                    for label, field in zip(self._get_labels(self.list_display),
                                            self.list_display)],
                 'obj': obj})
        return super(UserAdmin, self).render_change_form(
            request, context, add, change, form_url, obj)

    # Utils.

    @staticmethod
    def make_tracking_queryset(orig_queryset):
        queryset = orig_queryset.annotate(
            comment_count=Count('comment', distinct=True)
        )
        request_count_dict = dict(orig_queryset.filter(
            marketitem__item_type='request').annotate(
                request_count=Count('marketitem')
            ).values_list('id', 'request_count'))
        offer_count_dict = dict(orig_queryset.filter(
            marketitem__item_type='offer').annotate(
                offer_count=Count('marketitem')
            ).values_list('id', 'offer_count'))

        users = queryset[:]
        for user in users:
            user.request_count = request_count_dict.get(user.id, 0)
            user.offer_count = offer_count_dict.get(user.id, 0)
        return users

admin.site.register(UserTracking, UserAdmin)
