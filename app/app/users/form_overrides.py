from django.contrib.auth.models import User
from django.db.models import Q
from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm

class ResetPasswordFormSilent(ResetPasswordForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = User.objects \
            .filter(Q(email__iexact=email)
                    | Q(emailaddress__email__iexact=email)).distinct()
        if not self.users.exists():
            self.cleaned_data["email"] = 'silentreject@exchangivist.org'
        return self.cleaned_data["email"]
