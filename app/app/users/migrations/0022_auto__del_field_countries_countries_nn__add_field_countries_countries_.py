# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Countries.countries_nn'
        db.delete_column(u'users_countries', 'countries_nn')

        # Adding field 'Countries.countries_ar'
        db.add_column(u'users_countries', 'countries_ar',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Countries.countries_ru'
        db.add_column(u'users_countries', 'countries_ru',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Countries.countries_zh_cn'
        db.add_column(u'users_countries', 'countries_zh_cn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Skills.skills_nn'
        db.delete_column(u'users_skills', 'skills_nn')

        # Adding field 'Skills.skills_ar'
        db.add_column(u'users_skills', 'skills_ar',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Skills.skills_ru'
        db.add_column(u'users_skills', 'skills_ru',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Skills.skills_zh_cn'
        db.add_column(u'users_skills', 'skills_zh_cn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Residence.residence_nn'
        db.delete_column(u'users_residence', 'residence_nn')

        # Adding field 'Residence.residence_ar'
        db.add_column(u'users_residence', 'residence_ar',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Residence.residence_ru'
        db.add_column(u'users_residence', 'residence_ru',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Residence.residence_zh_cn'
        db.add_column(u'users_residence', 'residence_zh_cn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Issues.issues_nn'
        db.delete_column(u'users_issues', 'issues_nn')

        # Adding field 'Issues.issues_ar'
        db.add_column(u'users_issues', 'issues_ar',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Issues.issues_ru'
        db.add_column(u'users_issues', 'issues_ru',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Issues.issues_zh_cn'
        db.add_column(u'users_issues', 'issues_zh_cn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Nationality.nationality_nn'
        db.delete_column(u'users_nationality', 'nationality_nn')

        # Adding field 'Nationality.nationality_ar'
        db.add_column(u'users_nationality', 'nationality_ar',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Nationality.nationality_ru'
        db.add_column(u'users_nationality', 'nationality_ru',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Nationality.nationality_zh_cn'
        db.add_column(u'users_nationality', 'nationality_zh_cn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Countries.countries_nn'
        db.add_column(u'users_countries', 'countries_nn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Countries.countries_ar'
        db.delete_column(u'users_countries', 'countries_ar')

        # Deleting field 'Countries.countries_ru'
        db.delete_column(u'users_countries', 'countries_ru')

        # Deleting field 'Countries.countries_zh_cn'
        db.delete_column(u'users_countries', 'countries_zh_cn')

        # Adding field 'Skills.skills_nn'
        db.add_column(u'users_skills', 'skills_nn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Skills.skills_ar'
        db.delete_column(u'users_skills', 'skills_ar')

        # Deleting field 'Skills.skills_ru'
        db.delete_column(u'users_skills', 'skills_ru')

        # Deleting field 'Skills.skills_zh_cn'
        db.delete_column(u'users_skills', 'skills_zh_cn')

        # Adding field 'Residence.residence_nn'
        db.add_column(u'users_residence', 'residence_nn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Residence.residence_ar'
        db.delete_column(u'users_residence', 'residence_ar')

        # Deleting field 'Residence.residence_ru'
        db.delete_column(u'users_residence', 'residence_ru')

        # Deleting field 'Residence.residence_zh_cn'
        db.delete_column(u'users_residence', 'residence_zh_cn')

        # Adding field 'Issues.issues_nn'
        db.add_column(u'users_issues', 'issues_nn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Issues.issues_ar'
        db.delete_column(u'users_issues', 'issues_ar')

        # Deleting field 'Issues.issues_ru'
        db.delete_column(u'users_issues', 'issues_ru')

        # Deleting field 'Issues.issues_zh_cn'
        db.delete_column(u'users_issues', 'issues_zh_cn')

        # Adding field 'Nationality.nationality_nn'
        db.add_column(u'users_nationality', 'nationality_nn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Nationality.nationality_ar'
        db.delete_column(u'users_nationality', 'nationality_ar')

        # Deleting field 'Nationality.nationality_ru'
        db.delete_column(u'users_nationality', 'nationality_ru')

        # Deleting field 'Nationality.nationality_zh_cn'
        db.delete_column(u'users_nationality', 'nationality_zh_cn')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'users.countries': {
            'Meta': {'ordering': "['countries']", 'object_name': 'Countries'},
            'countries': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'countries_ar': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'countries_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'countries_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'countries_zh_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'users.issues': {
            'Meta': {'ordering': "['issues']", 'object_name': 'Issues'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issues': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'issues_ar': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'issues_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'issues_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'issues_zh_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'users.nationality': {
            'Meta': {'ordering': "['nationality']", 'object_name': 'Nationality'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nationality_ar': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nationality_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nationality_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nationality_zh_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'users.organisationalrating': {
            'Meta': {'object_name': 'OrganisationalRating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rated_by_ahr': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'users.residence': {
            'Meta': {'ordering': "['residence']", 'object_name': 'Residence'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'residence': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'residence_ar': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'residence_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'residence_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'residence_zh_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'users.skills': {
            'Meta': {'ordering': "['skills']", 'object_name': 'Skills'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skills': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'skills_ar': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'skills_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'skills_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'skills_zh_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Countries']", 'null': 'True', 'symmetrical': 'False'}),
            'expertise': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fb_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'firstlogin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'get_newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface_lang': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '3'}),
            'is_individual': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_journalist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_organisation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issues': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Issues']", 'null': 'True', 'symmetrical': 'False'}),
            'linkedin_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nationality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Nationality']", 'null': 'True'}),
            'notifications': ('json_field.fields.JSONField', [], {'default': "u'null'", 'null': 'True', 'blank': 'True'}),
            'notperm': ('json_field.fields.JSONField', [], {'default': "u'null'", 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'privacy_settings': ('json_field.fields.JSONField', [], {'default': "u'null'", 'null': 'True', 'blank': 'True'}),
            'ratecount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resident_country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Residence']", 'null': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Skills']", 'null': 'True', 'symmetrical': 'False'}),
            'tag_ling': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tweet_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'web_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'users.userrate': {
            'Meta': {'object_name': 'UserRate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rates'", 'null': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['users']