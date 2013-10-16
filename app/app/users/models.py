from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

import uuid

def user_image_upload_path_handler(instance, filename):
    return 'user/img/{file}'.format(file=str(uuid.uuid1()))

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	image = ImageField(upload_to=user_image_upload_path_handler)
	web_url = models.CharField(_('website url'), max_length=255, null=True, blank=True)
	fb_url = models.CharField(_('facebook page'), max_length=255, null=True, blank=True)
	tweet_url = models.CharField(_('twitter page'), max_length=255, null=True, blank=True)
	

	def save(self, *args, **kwargs):
		model = self.__class__
		try:
			this = UserProfile.objects.get(id=self.id)
			if this.image != self.image:
				this.image.delete(save=False)
		except:
			return

class Skills(models.Model):
	pass

class UserSkills(models.Model):
	pass


class Issues(models.Model):
	pass

class UserIssues(models.Model):
	pass


class Countries(models.Model):
	pass

class UserCountries(models.Model):
	pass