# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Placeholder.noinline'
        db.add_column('editable_placeholder', 'noinline',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Placeholder.noinline'
        db.delete_column('editable_placeholder', 'noinline')


    models = {
        'editable.placeholder': {
            'Meta': {'ordering': "['location']", 'object_name': 'Placeholder'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '1500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'noinline': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['editable']