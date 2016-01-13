# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MarketItemRelatedPost'
        db.create_table(u'market_marketitemrelatedpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('market_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['market.MarketItem'])),
            ('related_market_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_market_item', to=orm['market.MarketItem'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('market', ['MarketItemRelatedPost'])


        # Changing field 'MarketItemDirectOffer.details'
        db.alter_column(u'market_marketitemdirectoffer', 'details', self.gf('tinymce.models.HTMLField')(default=''))

    def backwards(self, orm):
        # Deleting model 'MarketItemRelatedPost'
        db.delete_table(u'market_marketitemrelatedpost')


        # Changing field 'MarketItemDirectOffer.details'
        db.alter_column(u'market_marketitemdirectoffer', 'details', self.gf('tinymce.models.HTMLField')(null=True))

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
            'contents': ('django.db.models.fields.TextField', [], {}),
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
            'needs_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'owner_candidate': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'commenttranslation_candidate'", 'null': 'True', 'to': u"orm['auth.User']"}),
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
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'date_of_action': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
        'market.marketitemdirectoffer': {
            'Meta': {'object_name': 'MarketItemDirectOffer'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'details': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['users.Interest']", 'null': 'True', 'blank': 'True'}),
            'market_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'specific_interest': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'market.marketitemhidden': {
            'Meta': {'object_name': 'MarketItemHidden'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"}),
            'viewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'market.marketitemhowcanyouhelp': {
            'Meta': {'object_name': 'MarketItemHowCanYouHelp'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'market.marketitemimage': {
            'Meta': {'object_name': 'MarketItemImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"}),
            'original': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'original_metadata': ('django.db.models.fields.TextField', [], {})
        },
        'market.marketitemnextsteps': {
            'Meta': {'object_name': 'MarketItemNextSteps'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_of_action': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
        'market.marketitemrelatedpost': {
            'Meta': {'object_name': 'MarketItemRelatedPost'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['market.MarketItem']"}),
            'related_market_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_market_item'", 'to': "orm['market.MarketItem']"})
        },
        'market.marketitemsalesforcerecord': {
            'Meta': {'object_name': 'MarketItemSalesforceRecord'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'salesforce'", 'unique': 'True', 'to': "orm['market.MarketItem']"}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'needs_updating': ('django.db.models.fields.BooleanField', [], {}),
            'salesforce_record_id': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
            'needs_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'owner_candidate': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'marketitemtranslation_candidate'", 'null': 'True', 'to': u"orm['auth.User']"}),
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
        'market.marketnewsitemdata': {
            'Meta': {'object_name': 'MarketNewsItemData'},
            'author_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'author_url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'image_field': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_scraped': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'market_item': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['market.MarketItem']", 'unique': 'True'}),
            'original_url': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'published': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
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
            'seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('json_field.fields.JSONField', [], {'default': "u'null'"}),
            'translation': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'max_length': '1', 'null': 'True'}),
            'translation_count': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
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
            'countries_fa': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'countries_fr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'name_fa': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'issues_fa': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'issues_fr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'name_fa': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_zh_cn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['market']