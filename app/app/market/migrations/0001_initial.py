# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resource'
        db.create_table(u'market_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('details', self.gf('tinymce.models.HTMLField')()),
            ('ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, blank=True)),
            ('comments', self.gf('json_field.fields.JSONField')(default=u'null', blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 11, 0, 0))),
            ('exp_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('afile', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'market', ['Resource'])

        # Adding M2M table for field countries on 'Resource'
        m2m_table_name = db.shorten_name(u'market_resource_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm[u'market.resource'], null=False)),
            ('countries', models.ForeignKey(orm[u'users.countries'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resource_id', 'countries_id'])

        # Adding M2M table for field issues on 'Resource'
        m2m_table_name = db.shorten_name(u'market_resource_issues')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm[u'market.resource'], null=False)),
            ('issues', models.ForeignKey(orm[u'users.issues'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resource_id', 'issues_id'])

        # Adding M2M table for field skills on 'Resource'
        m2m_table_name = db.shorten_name(u'market_resource_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm[u'market.resource'], null=False)),
            ('skills', models.ForeignKey(orm[u'users.skills'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resource_id', 'skills_id'])

        # Adding model 'Offer'
        db.create_table(u'market_offer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('details', self.gf('tinymce.models.HTMLField')()),
            ('ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, blank=True)),
            ('comments', self.gf('json_field.fields.JSONField')(default=u'null', blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 11, 0, 0))),
            ('exp_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'market', ['Offer'])

        # Adding M2M table for field countries on 'Offer'
        m2m_table_name = db.shorten_name(u'market_offer_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm[u'market.offer'], null=False)),
            ('countries', models.ForeignKey(orm[u'users.countries'], null=False))
        ))
        db.create_unique(m2m_table_name, ['offer_id', 'countries_id'])

        # Adding M2M table for field issues on 'Offer'
        m2m_table_name = db.shorten_name(u'market_offer_issues')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm[u'market.offer'], null=False)),
            ('issues', models.ForeignKey(orm[u'users.issues'], null=False))
        ))
        db.create_unique(m2m_table_name, ['offer_id', 'issues_id'])

        # Adding M2M table for field skills on 'Offer'
        m2m_table_name = db.shorten_name(u'market_offer_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm[u'market.offer'], null=False)),
            ('skills', models.ForeignKey(orm[u'users.skills'], null=False))
        ))
        db.create_unique(m2m_table_name, ['offer_id', 'skills_id'])

        # Adding model 'Request'
        db.create_table(u'market_request', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('details', self.gf('tinymce.models.HTMLField')()),
            ('ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, blank=True)),
            ('comments', self.gf('json_field.fields.JSONField')(default=u'null', blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 11, 0, 0))),
            ('exp_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'market', ['Request'])

        # Adding M2M table for field countries on 'Request'
        m2m_table_name = db.shorten_name(u'market_request_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('request', models.ForeignKey(orm[u'market.request'], null=False)),
            ('countries', models.ForeignKey(orm[u'users.countries'], null=False))
        ))
        db.create_unique(m2m_table_name, ['request_id', 'countries_id'])

        # Adding M2M table for field issues on 'Request'
        m2m_table_name = db.shorten_name(u'market_request_issues')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('request', models.ForeignKey(orm[u'market.request'], null=False)),
            ('issues', models.ForeignKey(orm[u'users.issues'], null=False))
        ))
        db.create_unique(m2m_table_name, ['request_id', 'issues_id'])


    def backwards(self, orm):
        # Deleting model 'Resource'
        db.delete_table(u'market_resource')

        # Removing M2M table for field countries on 'Resource'
        db.delete_table(db.shorten_name(u'market_resource_countries'))

        # Removing M2M table for field issues on 'Resource'
        db.delete_table(db.shorten_name(u'market_resource_issues'))

        # Removing M2M table for field skills on 'Resource'
        db.delete_table(db.shorten_name(u'market_resource_skills'))

        # Deleting model 'Offer'
        db.delete_table(u'market_offer')

        # Removing M2M table for field countries on 'Offer'
        db.delete_table(db.shorten_name(u'market_offer_countries'))

        # Removing M2M table for field issues on 'Offer'
        db.delete_table(db.shorten_name(u'market_offer_issues'))

        # Removing M2M table for field skills on 'Offer'
        db.delete_table(db.shorten_name(u'market_offer_skills'))

        # Deleting model 'Request'
        db.delete_table(u'market_request')

        # Removing M2M table for field countries on 'Request'
        db.delete_table(db.shorten_name(u'market_request_countries'))

        # Removing M2M table for field issues on 'Request'
        db.delete_table(db.shorten_name(u'market_request_issues'))


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
        u'market.offer': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'Offer'},
            'comments': ('json_field.fields.JSONField', [], {'default': "u'null'", 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Countries']", 'symmetrical': 'False'}),
            'details': ('tinymce.models.HTMLField', [], {}),
            'exp_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'blank': 'True'}),
            'issues': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Issues']", 'symmetrical': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 11, 0, 0)'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Skills']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'market.request': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'Request'},
            'comments': ('json_field.fields.JSONField', [], {'default': "u'null'", 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Countries']", 'symmetrical': 'False'}),
            'details': ('tinymce.models.HTMLField', [], {}),
            'exp_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'blank': 'True'}),
            'issues': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Issues']", 'symmetrical': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 11, 0, 0)'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'market.resource': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'Resource'},
            'afile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'comments': ('json_field.fields.JSONField', [], {'default': "u'null'", 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Countries']", 'symmetrical': 'False'}),
            'details': ('tinymce.models.HTMLField', [], {}),
            'exp_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'blank': 'True'}),
            'issues': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Issues']", 'symmetrical': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 11, 0, 0)'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Skills']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'users.countries': {
            'Meta': {'object_name': 'Countries'},
            'countries': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'users.issues': {
            'Meta': {'object_name': 'Issues'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issues': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'users.skills': {
            'Meta': {'object_name': 'Skills'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skills': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['market']