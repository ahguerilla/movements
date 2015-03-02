# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CommentTranslation'
        db.create_table(u'market_commenttranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('source_language', self.gf('django.db.models.fields.CharField')(default='en', max_length=10)),
            ('details_translated', self.gf('django.db.models.fields.TextField')()),
            ('details_candidate', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('generated_at', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, max_length=1)),
            ('c_status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, max_length=1)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('owner_candidate', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='commenttranslation_candidate', null=True, to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('timer', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('reminder', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['market.Comment'])),
        ))
        db.send_create_signal('market', ['CommentTranslation'])

        # Adding field 'MarketItemTranslation.details_candidate'
        db.add_column(u'market_marketitemtranslation', 'details_candidate',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'MarketItemTranslation.status'
        db.add_column(u'market_marketitemtranslation', 'status',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, max_length=1),
                      keep_default=False)

        # Adding field 'MarketItemTranslation.c_status'
        db.add_column(u'market_marketitemtranslation', 'c_status',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, max_length=1),
                      keep_default=False)

        # Adding field 'MarketItemTranslation.owner'
        db.add_column(u'market_marketitemtranslation', 'owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'MarketItemTranslation.owner_candidate'
        db.add_column(u'market_marketitemtranslation', 'owner_candidate',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='marketitemtranslation_candidate', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'MarketItemTranslation.created'
        db.add_column(u'market_marketitemtranslation', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2015, 2, 25, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'MarketItemTranslation.edited'
        db.add_column(u'market_marketitemtranslation', 'edited',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2015, 2, 25, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'MarketItemTranslation.timer'
        db.add_column(u'market_marketitemtranslation', 'timer',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'MarketItemTranslation.reminder'
        db.add_column(u'market_marketitemtranslation', 'reminder',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'MarketItemTranslation.title_candidate'
        db.add_column(u'market_marketitemtranslation', 'title_candidate',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Notification.translation'
        db.add_column(u'market_notification', 'translation',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, max_length=1),
                      keep_default=False)

        # Adding field 'Notification.timeto'
        db.add_column(u'market_notification', 'timeto',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Notification.reminder'
        db.add_column(u'market_notification', 'reminder',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'MarketItem.language'
        db.add_column(u'market_marketitem', 'language',
                      self.gf('django.db.models.fields.CharField')(default='en', max_length=10),
                      keep_default=False)

        # Adding field 'Comment.language'
        db.add_column(u'market_comment', 'language',
                      self.gf('django.db.models.fields.CharField')(default='en', max_length=10),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'CommentTranslation'
        db.delete_table(u'market_commenttranslation')

        # Deleting field 'MarketItemTranslation.details_candidate'
        db.delete_column(u'market_marketitemtranslation', 'details_candidate')

        # Deleting field 'MarketItemTranslation.status'
        db.delete_column(u'market_marketitemtranslation', 'status')

        # Deleting field 'MarketItemTranslation.c_status'
        db.delete_column(u'market_marketitemtranslation', 'c_status')

        # Deleting field 'MarketItemTranslation.owner'
        db.delete_column(u'market_marketitemtranslation', 'owner_id')

        # Deleting field 'MarketItemTranslation.owner_candidate'
        db.delete_column(u'market_marketitemtranslation', 'owner_candidate_id')

        # Deleting field 'MarketItemTranslation.created'
        db.delete_column(u'market_marketitemtranslation', 'created')

        # Deleting field 'MarketItemTranslation.edited'
        db.delete_column(u'market_marketitemtranslation', 'edited')

        # Deleting field 'MarketItemTranslation.timer'
        db.delete_column(u'market_marketitemtranslation', 'timer')

        # Deleting field 'MarketItemTranslation.reminder'
        db.delete_column(u'market_marketitemtranslation', 'reminder')

        # Deleting field 'MarketItemTranslation.title_candidate'
        db.delete_column(u'market_marketitemtranslation', 'title_candidate')

        # Deleting field 'Notification.translation'
        db.delete_column(u'market_notification', 'translation')

        # Deleting field 'Notification.timeto'
        db.delete_column(u'market_notification', 'timeto')

        # Deleting field 'Notification.reminder'
        db.delete_column(u'market_notification', 'reminder')

        # Deleting field 'MarketItem.language'
        db.delete_column(u'market_marketitem', 'language')

        # Deleting field 'Comment.language'
        db.delete_column(u'market_comment', 'language')


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
        'market.comment': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Comment'},
            'contents': ('tinymce.models.HTMLField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comments'", 'null': 'True', 'to': "orm['market.MarketItem']"}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'market.commenttranslation': {
            'Meta': {'object_name': 'CommentTranslation'},
            'c_status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'max_length': '1'}),
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.Comment']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details_candidate': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'details_translated': ('django.db.models.fields.TextField', [], {}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'generated_at': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'owner_candidate': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'commenttranslation_candidate'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'reminder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source_language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'max_length': '1'}),
            'timer': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'market.emailrecommendation': {
            'Meta': {'object_name': 'EmailRecommendation'},
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']", 'null': 'True'}),
            'recommendation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'market.itemrate': {
            'Meta': {'object_name': 'ItemRate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rates'", 'null': 'True', 'to': "orm['market.MarketItem']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'market.marketitem': {
            'Meta': {'object_name': 'MarketItem'},
            'closed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'collaboratorcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'commentcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['users.Countries']", 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'details': ('tinymce.models.HTMLField', [], {}),
            'featured_order_hint': ('django.db.models.fields.CharField', [], {'default': "'c'", 'max_length': '5'}),
            'feedback_response': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['users.Interest']", 'null': 'True', 'blank': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issues': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['users.Issues']", 'null': 'True', 'blank': 'True'}),
            'item_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ratecount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'receive_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'reportcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'specific_issue': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'specific_skill': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'staff_owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'marketitems'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tweet_permission': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        'market.marketitemactions': {
            'Meta': {'object_name': 'MarketItemActions'},
            'action': ('django.db.models.fields.TextField', [], {}),
            'date_of_action': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"})
        },
        'market.marketitemcollaborators': {
            'Meta': {'object_name': 'MarketItemCollaborators'},
            'collaborator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interaction_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'interaction_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'market_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"})
        },
        'market.marketitemhidden': {
            'Meta': {'object_name': 'MarketItemHidden'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"}),
            'viewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'market.marketitemnextsteps': {
            'Meta': {'object_name': 'MarketItemNextSteps'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_of_action': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"}),
            'next_step': ('django.db.models.fields.TextField', [], {})
        },
        'market.marketitempostreport': {
            'Meta': {'ordering': "['-resolved', '-pub_date']", 'object_name': 'MarketItemPostReport'},
            'contents': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repots'", 'null': 'True', 'to': "orm['market.MarketItem']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'resolved': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'market.marketitemstick': {
            'Meta': {'object_name': 'MarketItemStick'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"}),
            'viewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'market.marketitemtranslation': {
            'Meta': {'object_name': 'MarketItemTranslation'},
            'c_status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'max_length': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details_candidate': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'details_translated': ('django.db.models.fields.TextField', [], {}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'generated_at': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'market_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'owner_candidate': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'marketitemtranslation_candidate'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'reminder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source_language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'max_length': '1'}),
            'timer': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'title_candidate': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title_translated': ('django.db.models.fields.TextField', [], {})
        },
        'market.marketitemviewcounter': {
            'Meta': {'object_name': 'MarketItemViewCounter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"}),
            'viewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'market.messageext': {
            'Meta': {'ordering': "('-sent_at', '-id')", 'object_name': 'MessageExt', '_ormbases': [u'postman.Message']},
            'is_post_recommendation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_user_recommendation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'market_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']", 'null': 'True', 'blank': 'True'}),
            u'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['postman.Message']", 'unique': 'True', 'primary_key': 'True'})
        },
        'market.notification': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Notification'},
            'avatar_user': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.Comment']", 'null': 'True', 'blank': 'True'}),
            'emailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'reminder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('json_field.fields.JSONField', [], {'default': "u'null'"}),
            'timeto': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'translation': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'market.question': {
            'Meta': {'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'question_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'market.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['market.Question']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'market.userreport': {
            'Meta': {'ordering': "['-resolved', '-pub_date']", 'object_name': 'UserReport'},
            'contents': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'resolved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_repots'", 'to': u"orm['auth.User']"})
        },
        u'postman.message': {
            'Meta': {'ordering': "[u'-sent_at', u'-id']", 'object_name': 'Message'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderation_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'moderated_messages'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'moderation_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'moderation_reason': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            'moderation_status': ('django.db.models.fields.CharField', [], {'default': "u'p'", 'max_length': '1'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'next_messages'", 'null': 'True', 'to': u"orm['postman.Message']"}),
            'read_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'received_messages'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'recipient_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient_deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'replied_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'sent_messages'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'sender_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sender_deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'child_messages'", 'null': 'True', 'to': u"orm['postman.Message']"})
        },
        u'users.countries': {
            'Meta': {'ordering': "['countries']", 'object_name': 'Countries'},
            'countries': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'countries_ar': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'countries_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'countries_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'countries_uk': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'countries_zh_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Region']", 'null': 'True'})
        },
        u'users.interest': {
            'Meta': {'ordering': "['name']", 'object_name': 'Interest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'name_ar': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_zh_cn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'users.issues': {
            'Meta': {'ordering': "['issues']", 'object_name': 'Issues'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issues': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'issues_ar': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'issues_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'issues_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'issues_uk': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'issues_zh_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'users.region': {
            'Meta': {'object_name': 'Region'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'name_ar': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_zh_cn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['market']