# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Placeholder'
        db.create_table('editable_placeholder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=1500)),
        ))
        db.send_create_signal('editable', ['Placeholder'])


    def backwards(self, orm):
        # Deleting model 'Placeholder'
        db.delete_table('editable_placeholder')


    models = {
        'editable.placeholder': {
            'Meta': {'ordering': "['location']", 'object_name': 'Placeholder'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '1500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['editable']