from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
     #Optional. Comment out or delete if DO NOT WANT
     url(r'^login/$', 'django.contrib.auth.views.login', kwargs={'template_name': 'login.html'}, name="login"),

     # Optional. Same as above.
     url(r'^logout/$', 'django.contrib.auth.views.logout', kwargs={'template_name': 'logout.html'}, name="logout"),

     # If you want to add a custom template file, add kwargs={'template_name':
     # NAME_OF_TEMPLATE } before 'name="edit"'
     url(r'^(?P<location_name>\w+)$', 'app.editable.views.admin_edit', name="edit"),
)
