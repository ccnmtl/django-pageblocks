from django.db import models
from pagetree.models import PageBlock
from settings import MEDIA_ROOT
from sorl.thumbnail.fields import ImageWithThumbnailsField
from django.contrib.contenttypes import generic
from django import forms
import os
from django.template.defaultfilters import slugify
from datetime import datetime


class TextBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    body = models.TextField(blank=True)

    template_file = "pageblocks/textblock.html"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def edit_form(self):
        class EditForm(forms.Form):
            body = forms.CharField(widget=forms.widgets.Textarea(),
                                   initial=self.body)
        return EditForm()

    def edit(self,vals,files):
        self.body = vals.get('body','')
        self.save()

class HTMLBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    html = models.TextField(blank=True)

    template_file = "pageblocks/htmlblock.html"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def edit_form(self):
        class EditForm(forms.Form):
            html = forms.CharField(initial=self.html,
                                   widget=forms.widgets.Textarea())
        return EditForm()

    def edit(self,vals,files):
        self.html = vals.get('html','')
        self.save()


class PullQuoteBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    body = models.TextField(blank=True)
    template_file = "pageblocks/pullquoteblock.html"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def edit_form(self):
        class EditForm(forms.Form):
            body = forms.CharField(widget=forms.widgets.Textarea(),
                                   initial=self.body)
        return EditForm()

    def edit(self,vals,files):
        self.body = vals.get('body','')
        self.save()

class ImageBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    image = ImageWithThumbnailsField(upload_to="images/%Y/%m/%d",
                                     thumbnail = {
            'size' : (65,65)
            },
                                     extra_thumbnails={
            'admin': {
                'size': (70, 50),
                'options': ('sharpen',),
                }
            }
                                     )
    caption = models.TextField(blank=True)

    template_file = "pageblocks/imageblock.html"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def edit_form(self):
        class EditForm(forms.Form):
            image = forms.FileField(label="replace image")
            caption = forms.CharField(initial=self.caption,
                                      widget=forms.widgets.Textarea())
        return EditForm()

    def edit(self,vals,files):
        self.caption = vals.get('caption','')
        if 'image' in files:
            self.save_image(files['image'])
        self.save()

    def save_image(self,f):
        ext = f.name.split(".")[-1].lower()
        basename = slugify(f.name.split(".")[-2].lower())[:20]
        if ext not in ['jpg','jpeg','gif','png']:
            # unsupported image format
            return None
        now = datetime.now()
        path = "images/%04d/%02d/%02d/" % (now.year,now.month,now.day)
        try:
            os.makedirs(MEDIA_ROOT + "/" + path)
        except:
            pass
        full_filename = path + "%s.%s" % (basename,ext)
        fd = open(MEDIA_ROOT + "/" + full_filename,'wb')
        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename



class ImagePullQuoteBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    image = ImageWithThumbnailsField(upload_to="images/%Y/%m/%d",
                                     thumbnail = {
            'size' : (65,65)
            },
                                     extra_thumbnails={
            'admin': {
                'size': (70, 50),
                'options': ('sharpen',),
                }
            }
                                     )
    caption = models.TextField(blank=True)

    template_file = "pageblocks/imagepullquoteblock.html"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def edit_form(self):
        class EditForm(forms.Form):
            image = forms.FileField(label="replace image")
            caption = forms.CharField(initial=self.caption,
                                      widget=forms.widgets.Textarea())
        return EditForm()

    def edit(self,vals,files):
        self.caption = vals.get('caption','')
        if 'image' in files:
            self.save_image(files['image'])
        self.save()

    def save_image(self,f):
        ext = f.name.split(".")[-1].lower()
        basename = slugify(f.name.split(".")[-2].lower())[:20]
        if ext not in ['jpg','jpeg','gif','png']:
            # unsupported image format
            return None
        now = datetime.now()
        path = "images/%04d/%02d/%02d/" % (now.year,now.month,now.day)
        try:
            os.makedirs(MEDIA_ROOT + "/" + path)
        except:
            pass
        full_filename = path + "%s.%s" % (basename,ext)
        fd = open(MEDIA_ROOT + "/" + full_filename,'wb')
        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename


    

class ImagePullQuoteBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    image = ImageWithThumbnailsField(upload_to="images/%Y/%m/%d",
                                     thumbnail = {
            'size' : (65,65)
            },
                                     extra_thumbnails={
            'admin': {
                'size': (70, 50),
                'options': ('sharpen',),
                }
            }
                                     )
    caption = models.TextField(blank=True)
    def pageblock(self):
        return self.pageblocks.all()[0]
