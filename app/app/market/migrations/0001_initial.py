# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MarketItemBase'
        db.create_table(u'market_marketitembase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('details', self.gf('tinymce.models.HTMLField')()),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('comments', self.gf('json_field.fields.JSONField')(default=u'null')),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 6, 0, 0))),
        ))
        db.send_create_signal(u'market', ['MarketItemBase'])

        # Adding M2M table for field countries on 'MarketItemBase'
        m2m_table_name = db.shorten_name(u'market_marketitembase_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('marketitembase', models.ForeignKey(orm[u'market.marketitembase'], null=False)),
            ('countries', models.ForeignKey(orm[u'users.countries'], null=False))
        ))
        db.create_unique(m2m_table_name, ['marketitembase_id', 'countries_id'])

        # Adding M2M table for field issues on 'MarketItemBase'
        m2m_table_name = db.shorten_name(u'market_marketitembase_issues')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('marketitembase', models.ForeignKey(orm[u'market.marketitembase'], null=False)),
            ('issues', models.ForeignKey(orm[u'users.issues'], null=False))
        ))
        db.create_unique(m2m_table_name, ['marketitembase_id', 'issues_id'])

        # Adding model 'Offer'
        db.create_table(u'market_offer', (
            (u'marketitembase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['market.MarketItemBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'market', ['Offer'])

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
            (u'marketitembase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['market.MarketItemBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'market', ['Request'])

        # Adding model 'Resource'
        db.create_table(u'market_resource', (
            (u'marketitembase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['market.MarketItemBase'], unique=True, primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('afile', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'market', ['Resource'])

        # Adding M2M table for field skills on 'Resource'
        m2m_table_name = db.shorten_name(u'market_resource_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm[u'market.resource'], null=False)),
            ('skills', models.ForeignKey(orm[u'users.skills'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resource_id', 'skills_id'])


    def backwards(self, orm):
        # Deleting model 'MarketItemBase'
        db.delete_table(u'market_marketitembase')

        # Removing M2M table for field countries on 'MarketItemBase'
        db.delete_table(db.shorten_name(u'market_marketitembase_countries'))

        # Removing M2M table for field issues on 'MarketItemBase'
        db.delete_table(db.shorten_name(u'market_marketitembase_issues'))

        # Deleting model 'Offer'
        db.delete_table(u'market_offer')

        # Removing M2M table for field skills on 'Offer'
        db.delete_table(db.shorten_name(u'market_offer_skills'))

        # Deleting model 'Request'
        db.delete_table(u'market_request')

        # Deleting model 'Resource'
        db.delete_table(u'market_resource')

        # Removing M2M table for field skills on 'Resource'
        db.delete_table(db.shorten_name(u'market_resource_skills'))


    models = {
        u'market.marketitembase': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'MarketItemBase'},
            'comments': ('json_field.fields.JSONField', [], {'default': "u'null'"}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Countries']", 'symmetrical': 'False'}),
            'details': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'issues': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Issues']", 'symmetrical': 'False'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 6, 0, 0)'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'market.offer': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'Offer', '_ormbases': [u'market.MarketItemBase']},
            u'marketitembase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['market.MarketItemBase']", 'unique': 'True', 'primary_key': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Skills']", 'symmetrical': 'False'})
        },
        u'market.request': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'Request', '_ormbases': [u'market.MarketItemBase']},
            u'marketitembase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['market.MarketItemBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'market.resource': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'Resource', '_ormbases': [u'market.MarketItemBase']},
            'afile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'marketitembase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['market.MarketItemBase']", 'unique': 'True', 'primary_key': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Skills']", 'symmetrical': 'False'}),
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