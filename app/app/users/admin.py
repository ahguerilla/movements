from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from app.users.models import UserProfile, Countries, Skills, Issues, Nationality
from django.contrib.admin.models import LogEntry
from modeltranslation.admin import TranslationAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'vetting' ,'vetted_by')

    def vetting(self, obj):
        if obj.is_staff:
            return 'Staff'
        result = 'Vetted' if obj.is_active else 'Not Vetted'
        vet_url = reverse('vet_user', args=(obj.id,))
        return u'<a href="{0}" target="_blank" alt="vet user">Vet User</a> ({1})'.format(vet_url, result)
    vetting.process = 'Process'
    vetting.allow_tags = True

    def vetted_by(self,obj):
        log = LogEntry.objects.filter(object_id = obj.id).all()
        if len(log)>0:
            return log[0].user.username
        else:
            return ''

class SkillsAdmin(TranslationAdmin):
    list_display = ('skills',)

class CountriesAdmin(TranslationAdmin):
    list_display = ('countries',)

class IssuesAdmin(TranslationAdmin):
    list_display = ('issues',)

class NationalityAdmin(TranslationAdmin):
    list_display = ('nationality',)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Countries, CountriesAdmin)
admin.site.register(Skills, SkillsAdmin)
admin.site.register(Issues, IssuesAdmin)
admin.site.register(Nationality, NationalityAdmin)