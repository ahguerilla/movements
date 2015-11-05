# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HomePageBanner.title_text_ar'
        db.add_column(u'app_homepagebanner', 'title_text_ar',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.title_text_en'
        db.add_column(u'app_homepagebanner', 'title_text_en',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.title_text_zh_cn'
        db.add_column(u'app_homepagebanner', 'title_text_zh_cn',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.title_text_uk'
        db.add_column(u'app_homepagebanner', 'title_text_uk',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.title_text_ru'
        db.add_column(u'app_homepagebanner', 'title_text_ru',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.title_text_fa'
        db.add_column(u'app_homepagebanner', 'title_text_fa',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.title_text_fr'
        db.add_column(u'app_homepagebanner', 'title_text_fr',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.sub_text_ar'
        db.add_column(u'app_homepagebanner', 'sub_text_ar',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.sub_text_en'
        db.add_column(u'app_homepagebanner', 'sub_text_en',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.sub_text_zh_cn'
        db.add_column(u'app_homepagebanner', 'sub_text_zh_cn',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.sub_text_uk'
        db.add_column(u'app_homepagebanner', 'sub_text_uk',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.sub_text_ru'
        db.add_column(u'app_homepagebanner', 'sub_text_ru',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.sub_text_fa'
        db.add_column(u'app_homepagebanner', 'sub_text_fa',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HomePageBanner.sub_text_fr'
        db.add_column(u'app_homepagebanner', 'sub_text_fr',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'HomePageBanner.title_text_ar'
        db.delete_column(u'app_homepagebanner', 'title_text_ar')

        # Deleting field 'HomePageBanner.title_text_en'
        db.delete_column(u'app_homepagebanner', 'title_text_en')

        # Deleting field 'HomePageBanner.title_text_zh_cn'
        db.delete_column(u'app_homepagebanner', 'title_text_zh_cn')

        # Deleting field 'HomePageBanner.title_text_uk'
        db.delete_column(u'app_homepagebanner', 'title_text_uk')

        # Deleting field 'HomePageBanner.title_text_ru'
        db.delete_column(u'app_homepagebanner', 'title_text_ru')

        # Deleting field 'HomePageBanner.title_text_fa'
        db.delete_column(u'app_homepagebanner', 'title_text_fa')

        # Deleting field 'HomePageBanner.title_text_fr'
        db.delete_column(u'app_homepagebanner', 'title_text_fr')

        # Deleting field 'HomePageBanner.sub_text_ar'
        db.delete_column(u'app_homepagebanner', 'sub_text_ar')

        # Deleting field 'HomePageBanner.sub_text_en'
        db.delete_column(u'app_homepagebanner', 'sub_text_en')

        # Deleting field 'HomePageBanner.sub_text_zh_cn'
        db.delete_column(u'app_homepagebanner', 'sub_text_zh_cn')

        # Deleting field 'HomePageBanner.sub_text_uk'
        db.delete_column(u'app_homepagebanner', 'sub_text_uk')

        # Deleting field 'HomePageBanner.sub_text_ru'
        db.delete_column(u'app_homepagebanner', 'sub_text_ru')

        # Deleting field 'HomePageBanner.sub_text_fa'
        db.delete_column(u'app_homepagebanner', 'sub_text_fa')

        # Deleting field 'HomePageBanner.sub_text_fr'
        db.delete_column(u'app_homepagebanner', 'sub_text_fr')


    models = {
        u'app.homepagebanner': {
            'Meta': {'ordering': "('order',)", 'object_name': 'HomePageBanner'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sub_text': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'sub_text_ar': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'sub_text_en': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'sub_text_fa': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'sub_text_fr': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'sub_text_ru': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'sub_text_uk': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'sub_text_zh_cn': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_text_ar': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_text_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_text_fa': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_text_fr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_text_ru': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_text_uk': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_text_zh_cn': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'app.menuextension': {
            'Meta': {'object_name': 'MenuExtension'},
            'extended_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.Page']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_extension': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'draft_extension'", 'unique': 'True', 'null': 'True', 'to': u"orm['app.MenuExtension']"}),
            'show_on_footer_menu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_on_top_menu': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'app.newslettersignups': {
            'Meta': {'ordering': "('-registered_date',)", 'object_name': 'NewsletterSignups'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registered_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'app.notificationping': {
            'Meta': {'object_name': 'NotificationPing'},
            'completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_email_to': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        u'app.partner': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Partner'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'app.safevpnlink': {
            'Meta': {'object_name': 'SafeVPNLink', '_ormbases': ['cms.CMSPlugin']},
            'base_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'link_text': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'app.successstories': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SuccessStories'},
            'content': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'app.successstoriescmsplugin': {
            'Meta': {'object_name': 'SuccessStoriesCMSPlugin', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cms.page': {
            'Meta': {'ordering': "('path',)", 'unique_together': "(('publisher_is_draft', 'site', 'application_namespace'), ('reverse_id', 'site', 'publisher_is_draft'))", 'object_name': 'Page'},
            'application_namespace': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'application_urls': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'changed_by': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_home': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'languages': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'limit_visibility_in_menu': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'navigation_extenders': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['cms.Page']"}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'placeholders': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cms.Placeholder']", 'symmetrical': 'False'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'publication_end_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['cms.Page']"}),
            'reverse_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'revision_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'djangocms_pages'", 'to': u"orm['sites.Site']"}),
            'soft_root': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'INHERIT'", 'max_length': '100'}),
            'xframe_options': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['app']