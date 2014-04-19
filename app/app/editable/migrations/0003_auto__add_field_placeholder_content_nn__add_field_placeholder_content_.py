# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Placeholder.content_nn'
        db.add_column(u'editable_placeholder', 'content_nn',
                      self.gf('django.db.models.fields.TextField')(max_length=1500, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Placeholder.content_en'
        db.add_column(u'editable_placeholder', 'content_en',
                      self.gf('django.db.models.fields.TextField')(max_length=1500, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Placeholder.content_nn'
        db.delete_column(u'editable_placeholder', 'content_nn')

        # Deleting field 'Placeholder.content_en'
        db.delete_column(u'editable_placeholder', 'content_en')


    models = {
        u'editable.placeholder': {
            'Meta': {'ordering': "['location']", 'object_name': 'Placeholder'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '1500'}),
            'content_en': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'null': 'True', 'blank': 'True'}),
            'content_nn': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'noinline': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['editable']