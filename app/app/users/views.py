from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from models import UserProfile
from forms import SettingsForm
from allauth.account.views import SignupView

#@login_required(login_url='/accounts/login/')
def settings(request):
    if request.method == "POST":
        form = SettingsForm(request.POST)

        if form.is_valid():
            print('valid')
        else:
            print('not valid')
        
        password = request.POST.get('password')
        check = request.POST.get('check_password')
        if password != check:
            return render_to_response('users/usersettings.html', {
                'form': form,
            }, context_instance=RequestContext(request))

        cur_user = User.objects.get(id=request.user.id)
        cur_id = cur_user.id
        userprofile = UserProfile.objects.filter(user_id=cur_id)

        if not userprofile:
            print('No UserProfile')
            new_profile = UserProfile(user_id=cur_id)
            new_profile.save()

        update_profile = UserProfile(user_id=cur_id)
        #updated_profile.first_name = request.POST.get('first_name')
        #updated_profile.last_name = request.POST.get('last_name')
        update_profile.bio = request.POST.get('bio')
        update_profile.save()

    else:
        form = SettingsForm()

    return render_to_response('users/usersettings.html', {
            'form': form,
        }, context_instance=RequestContext(request))


class AccountSignupView(SignupView):
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields['first_name'].initial = self.request.GET.get('first_name', '')
        form.fields['last_name'].initial = self.request.GET.get('last_name', '')
        kwargs['form'] = form
        context = self.get_context_data(**kwargs)
        context['form'].fields['email'].initial = self.request.GET.get('email', '')
        return self.render_to_response(context)      

accountsignup = AccountSignupView.as_view()