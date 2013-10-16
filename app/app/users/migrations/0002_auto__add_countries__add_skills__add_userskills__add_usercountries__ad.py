# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Countries'
        db.create_table(u'users_countries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['Countries'])

        # Adding model 'Skills'
        db.create_table(u'users_skills', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['Skills'])

        # Adding model 'UserSkills'
        db.create_table(u'users_userskills', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['UserSkills'])

        # Adding model 'UserCountries'
        db.create_table(u'users_usercountries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['UserCountries'])

        # Adding model 'Issues'
        db.create_table(u'users_issues', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['Issues'])

        # Adding model 'UserIssues'
        db.create_table(u'users_userissues', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['UserIssues'])

        # Adding field 'UserProfile.tweet_url'
        db.add_column(u'users_userprofile', 'tweet_url',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


        # Changing field 'UserProfile.web_url'
        db.alter_column(u'users_userprofile', 'web_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'UserProfile.fb_url'
        db.alter_column(u'users_userprofile', 'fb_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):
        # Deleting model 'Countries'
        db.delete_table(u'users_countries')

        # Deleting model 'Skills'
        db.delete_table(u'users_skills')

        # Deleting model 'UserSkills'
        db.delete_table(u'users_userskills')

        # Deleting model 'UserCountries'
        db.delete_table(u'users_usercountries')

        # Deleting model 'Issues'
        db.delete_table(u'users_issues')

        # Deleting model 'UserIssues'
        db.delete_table(u'users_userissues')

        # Deleting field 'UserProfile.tweet_url'
        db.delete_column(u'users_userprofile', 'tweet_url')


        # User chose to not deal with backwards NULL issues for 'UserProfile.web_url'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.web_url' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'UserProfile.web_url'
        db.alter_column(u'users_userprofile', 'web_url', self.gf('django.db.models.fields.CharField')(max_length=255))

        # User chose to not deal with backwards NULL issues for 'UserProfile.fb_url'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.fb_url' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'UserProfile.fb_url'
        db.alter_column(u'users_userprofile', 'fb_url', self.gf('django.db.models.fields.CharField')(max_length=255))

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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
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
            'Meta': {'object_name': 'Countries'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'users.issues': {
            'Meta': {'object_name': 'Issues'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'users.skills': {
            'Meta': {'object_name': 'Skills'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'users.usercountries': {
            'Meta': {'object_name': 'UserCountries'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'users.userissues': {
            'Meta': {'object_name': 'UserIssues'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'fb_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'tweet_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'web_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'users.userskills': {
            'Meta': {'object_name': 'UserSkills'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['users']