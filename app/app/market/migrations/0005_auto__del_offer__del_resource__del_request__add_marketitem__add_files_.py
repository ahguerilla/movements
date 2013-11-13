# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Offer'
        db.delete_table(u'market_offer')

        # Removing M2M table for field issues on 'Offer'
        db.delete_table(db.shorten_name(u'market_offer_issues'))

        # Removing M2M table for field countries on 'Offer'
        db.delete_table(db.shorten_name(u'market_offer_countries'))

        # Removing M2M table for field skills on 'Offer'
        db.delete_table(db.shorten_name(u'market_offer_skills'))

        # Deleting model 'Resource'
        db.delete_table(u'market_resource')

        # Removing M2M table for field issues on 'Resource'
        db.delete_table(db.shorten_name(u'market_resource_issues'))

        # Removing M2M table for field countries on 'Resource'
        db.delete_table(db.shorten_name(u'market_resource_countries'))

        # Removing M2M table for field skills on 'Resource'
        db.delete_table(db.shorten_name(u'market_resource_skills'))

        # Deleting model 'Request'
        db.delete_table(u'market_request')

        # Removing M2M table for field issues on 'Request'
        db.delete_table(db.shorten_name(u'market_request_issues'))

        # Removing M2M table for field countries on 'Request'
        db.delete_table(db.shorten_name(u'market_request_countries'))

        # Adding model 'MarketItem'
        db.create_table(u'market_marketitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('details', self.gf('tinymce.models.HTMLField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 13, 0, 0))),
            ('exp_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'market', ['MarketItem'])

        # Adding M2M table for field countries on 'MarketItem'
        m2m_table_name = db.shorten_name(u'market_marketitem_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('marketitem', models.ForeignKey(orm[u'market.marketitem'], null=False)),
            ('countries', models.ForeignKey(orm[u'users.countries'], null=False))
        ))
        db.create_unique(m2m_table_name, ['marketitem_id', 'countries_id'])

        # Adding M2M table for field issues on 'MarketItem'
        m2m_table_name = db.shorten_name(u'market_marketitem_issues')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('marketitem', models.ForeignKey(orm[u'market.marketitem'], null=False)),
            ('issues', models.ForeignKey(orm[u'users.issues'], null=False))
        ))
        db.create_unique(m2m_table_name, ['marketitem_id', 'issues_id'])

        # Adding M2M table for field skills on 'MarketItem'
        m2m_table_name = db.shorten_name(u'market_marketitem_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('marketitem', models.ForeignKey(orm[u'market.marketitem'], null=False)),
            ('skills', models.ForeignKey(orm[u'users.skills'], null=False))
        ))
        db.create_unique(m2m_table_name, ['marketitem_id', 'skills_id'])

        # Adding model 'Files'
        db.create_table(u'market_files', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('afile', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['market.MarketItem'])),
        ))
        db.send_create_signal(u'market', ['Files'])

        # Adding field 'Comment.item'
        db.add_column(u'market_comment', 'item',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['market.MarketItem'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Offer'
        db.create_table(u'market_offer', (
            ('exp_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 13, 0, 0))),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comments', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['market.Comment'], null=True, blank=True)),
            ('details', self.gf('tinymce.models.HTMLField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'market', ['Offer'])

        # Adding M2M table for field issues on 'Offer'
        m2m_table_name = db.shorten_name(u'market_offer_issues')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm[u'market.offer'], null=False)),
            ('issues', models.ForeignKey(orm[u'users.issues'], null=False))
        ))
        db.create_unique(m2m_table_name, ['offer_id', 'issues_id'])

        # Adding M2M table for field countries on 'Offer'
        m2m_table_name = db.shorten_name(u'market_offer_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm[u'market.offer'], null=False)),
            ('countries', models.ForeignKey(orm[u'users.countries'], null=False))
        ))
        db.create_unique(m2m_table_name, ['offer_id', 'countries_id'])

        # Adding M2M table for field skills on 'Offer'
        m2m_table_name = db.shorten_name(u'market_offer_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm[u'market.offer'], null=False)),
            ('skills', models.ForeignKey(orm[u'users.skills'], null=False))
        ))
        db.create_unique(m2m_table_name, ['offer_id', 'skills_id'])

        # Adding model 'Resource'
        db.create_table(u'market_resource', (
            ('exp_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 13, 0, 0))),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comments', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['market.Comment'], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('details', self.gf('tinymce.models.HTMLField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('afile', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'market', ['Resource'])

        # Adding M2M table for field issues on 'Resource'
        m2m_table_name = db.shorten_name(u'market_resource_issues')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm[u'market.resource'], null=False)),
            ('issues', models.ForeignKey(orm[u'users.issues'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resource_id', 'issues_id'])

        # Adding M2M table for field countries on 'Resource'
        m2m_table_name = db.shorten_name(u'market_resource_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm[u'market.resource'], null=False)),
            ('countries', models.ForeignKey(orm[u'users.countries'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resource_id', 'countries_id'])

        # Adding M2M table for field skills on 'Resource'
        m2m_table_name = db.shorten_name(u'market_resource_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm[u'market.resource'], null=False)),
            ('skills', models.ForeignKey(orm[u'users.skills'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resource_id', 'skills_id'])

        # Adding model 'Request'
        db.create_table(u'market_request', (
            ('exp_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 13, 0, 0))),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comments', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['market.Comment'], null=True, blank=True)),
            ('details', self.gf('tinymce.models.HTMLField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'market', ['Request'])

        # Adding M2M table for field issues on 'Request'
        m2m_table_name = db.shorten_name(u'market_request_issues')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('request', models.ForeignKey(orm[u'market.request'], null=False)),
            ('issues', models.ForeignKey(orm[u'users.issues'], null=False))
        ))
        db.create_unique(m2m_table_name, ['request_id', 'issues_id'])

        # Adding M2M table for field countries on 'Request'
        m2m_table_name = db.shorten_name(u'market_request_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('request', models.ForeignKey(orm[u'market.request'], null=False)),
            ('countries', models.ForeignKey(orm[u'users.countries'], null=False))
        ))
        db.create_unique(m2m_table_name, ['request_id', 'countries_id'])

        # Deleting model 'MarketItem'
        db.delete_table(u'market_marketitem')

        # Removing M2M table for field countries on 'MarketItem'
        db.delete_table(db.shorten_name(u'market_marketitem_countries'))

        # Removing M2M table for field issues on 'MarketItem'
        db.delete_table(db.shorten_name(u'market_marketitem_issues'))

        # Removing M2M table for field skills on 'MarketItem'
        db.delete_table(db.shorten_name(u'market_marketitem_skills'))

        # Deleting model 'Files'
        db.delete_table(u'market_files')

        # Deleting field 'Comment.item'
        db.delete_column(u'market_comment', 'item_id')


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
        u'market.comment': {
            'Meta': {'object_name': 'Comment'},
            'contents': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['market.MarketItem']", 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 13, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'market.files': {
            'Meta': {'object_name': 'Files'},
            'afile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['market.MarketItem']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'market.marketitem': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'MarketItem'},
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Countries']", 'symmetrical': 'False'}),
            'details': ('tinymce.models.HTMLField', [], {}),
            'exp_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issues': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Issues']", 'symmetrical': 'False'}),
            'item_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 13, 0, 0)'}),
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