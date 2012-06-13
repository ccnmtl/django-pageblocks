# encoding: utf-8
# flake8: noqa
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TextBlock'
        db.create_table('pageblocks_textblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('pageblocks', ['TextBlock'])

        # Adding model 'HTMLBlock'
        db.create_table('pageblocks_htmlblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('pageblocks', ['HTMLBlock'])

        # Adding model 'PullQuoteBlock'
        db.create_table('pageblocks_pullquoteblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('pageblocks', ['PullQuoteBlock'])

        # Adding model 'ImageBlock'
        db.create_table('pageblocks_imageblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageWithThumbnailsField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('pageblocks', ['ImageBlock'])

        # Adding model 'ImagePullQuoteBlock'
        db.create_table('pageblocks_imagepullquoteblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageWithThumbnailsField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('pageblocks', ['ImagePullQuoteBlock'])

        # Adding model 'HTMLBlockWYSIWYG'
        db.create_table('pageblocks_htmlblockwysiwyg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wysiwyg_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('pageblocks', ['HTMLBlockWYSIWYG'])


    def backwards(self, orm):
        
        # Deleting model 'TextBlock'
        db.delete_table('pageblocks_textblock')

        # Deleting model 'HTMLBlock'
        db.delete_table('pageblocks_htmlblock')

        # Deleting model 'PullQuoteBlock'
        db.delete_table('pageblocks_pullquoteblock')

        # Deleting model 'ImageBlock'
        db.delete_table('pageblocks_imageblock')

        # Deleting model 'ImagePullQuoteBlock'
        db.delete_table('pageblocks_imagepullquoteblock')

        # Deleting model 'HTMLBlockWYSIWYG'
        db.delete_table('pageblocks_htmlblockwysiwyg')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pageblocks.htmlblock': {
            'Meta': {'object_name': 'HTMLBlock'},
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pageblocks.htmlblockwysiwyg': {
            'Meta': {'object_name': 'HTMLBlockWYSIWYG'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'wysiwyg_html': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'pageblocks.imageblock': {
            'Meta': {'object_name': 'ImageBlock'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageWithThumbnailsField', [], {'max_length': '100'})
        },
        'pageblocks.imagepullquoteblock': {
            'Meta': {'object_name': 'ImagePullQuoteBlock'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageWithThumbnailsField', [], {'max_length': '100'})
        },
        'pageblocks.pullquoteblock': {
            'Meta': {'object_name': 'PullQuoteBlock'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pageblocks.textblock': {
            'Meta': {'object_name': 'TextBlock'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pagetree.hierarchy': {
            'Meta': {'object_name': 'Hierarchy'},
            'base_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'pagetree.pageblock': {
            'Meta': {'ordering': "('section', 'ordinality')", 'object_name': 'PageBlock'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordinality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Section']"})
        },
        'pagetree.section': {
            'Meta': {'object_name': 'Section'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hierarchy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Hierarchy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['pageblocks']
