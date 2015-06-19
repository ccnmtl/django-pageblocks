# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SimpleImageBlock'
        db.create_table(u'pageblocks_simpleimageblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'pageblocks', ['SimpleImageBlock'])


    def backwards(self, orm):
        # Deleting model 'SimpleImageBlock'
        db.delete_table(u'pageblocks_simpleimageblock')


    models = {
        u'pageblocks.htmlblock': {
            'Meta': {'object_name': 'HTMLBlock'},
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pageblocks.htmlblockwysiwyg': {
            'Meta': {'object_name': 'HTMLBlockWYSIWYG'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'wysiwyg_html': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'pageblocks.imageblock': {
            'Meta': {'object_name': 'ImageBlock'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageWithThumbnailsField', [], {'max_length': '100'}),
            'lightbox': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'pageblocks.imagepullquoteblock': {
            'Meta': {'object_name': 'ImagePullQuoteBlock'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageWithThumbnailsField', [], {'max_length': '100'})
        },
        u'pageblocks.pullquoteblock': {
            'Meta': {'object_name': 'PullQuoteBlock'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pageblocks.simpleimageblock': {
            'Meta': {'object_name': 'SimpleImageBlock'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'pageblocks.textblock': {
            'Meta': {'object_name': 'TextBlock'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['pageblocks']