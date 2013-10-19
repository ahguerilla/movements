# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Countries'
        db.delete_table(u'users_countries')

        # Deleting model 'UserCountries'
        db.delete_table(u'users_usercountries')

        # Deleting model 'Issues'
        db.delete_table(u'users_issues')

        # Deleting model 'UserIssues'
        db.delete_table(u'users_userissues')

        # Deleting field 'Skills.skill'
        db.delete_column(u'users_skills', 'skill')

        # Adding field 'Skills.skills'
        db.add_column(u'users_skills', 'skills',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding M2M table for field skills on 'UserProfile'
        m2m_table_name = db.shorten_name(u'users_userprofile_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'users.userprofile'], null=False)),
            ('skills', models.ForeignKey(orm[u'users.skills'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'skills_id'])


    def backwards(self, orm):
        # Adding model 'Countries'
        db.create_table(u'users_countries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['Countries'])

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

        # Adding field 'Skills.skill'
        db.add_column(u'users_skills', 'skill',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Deleting field 'Skills.skills'
        db.delete_column(u'users_skills', 'skills')

        # Removing M2M table for field skills on 'UserProfile'
        db.delete_table(db.shorten_name(u'users_userprofile_skills'))


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
        u'users.skills': {
            'Meta': {'object_name': 'Skills'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skills': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'expertise': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fb_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'get_newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'is_journalist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_organisation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nationality': ('django.db.models.fields.CharField', [], {'default': "'AFG'", 'max_length': '3'}),
            'notifications': ('json_field.fields.JSONField', [], {'default': "u'null'"}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'privacy_settings': ('json_field.fields.JSONField', [], {'default': "u'null'"}),
            'resident_country': ('django.db.models.fields.CharField', [], {'default': "'AFG'", 'max_length': '3'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Skills']", 'symmetrical': 'False'}),
            'tweet_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'web_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['users']