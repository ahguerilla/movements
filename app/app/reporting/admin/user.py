# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ...market.models import MarketItemViewCounter
from ..models import UserTracking
from .base import TrackingAdmin


class UserAdmin(TrackingAdmin):
    list_select_related = ('userprofile',)
    list_display_links = ('id', 'get_screen_name')
    list_display = (
        'id', 'get_screen_name', 'get_signup_date', 'get_full_name',
        'get_nationality', 'get_resident_country', 'email',
        #'get_request_count', 'get_offer_count', 'get_comment_count',
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
        return orig_queryset
        # queryset = orig_queryset.annotate(
        #     comment_count=Count('comment', distinct=True)
        # )
        # request_count_dict = dict(orig_queryset.filter(
        #     marketitem__item_type='request').annotate(
        #         request_count=Count('marketitem')
        #     ).values_list('id', 'request_count'))
        # offer_count_dict = dict(orig_queryset.filter(
        #     marketitem__item_type='offer').annotate(
        #         offer_count=Count('marketitem')
        #     ).values_list('id', 'offer_count'))
        #
        # users = queryset[:]
        # for user in users:
        #     user.request_count = request_count_dict.get(user.id, 0)
        #     user.offer_count = offer_count_dict.get(user.id, 0)
        # return users

admin.site.register(UserTracking, UserAdmin)
