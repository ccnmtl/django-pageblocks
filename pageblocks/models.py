from django.db import models
from pagetree.models import PageBlock
from django.conf import settings
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
    display_name = "Text Block"

    def __unicode__(self):
        return unicode(self.pageblock())

    def pageblock(self):
        return self.pageblocks.all()[0]

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            body = forms.CharField(widget=forms.widgets.Textarea())
        return AddForm()

    @classmethod
    def create(self,request):
        return TextBlock.objects.create(body=request.POST.get('body',''))

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
    display_name = "HTML Block"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def edit_form(self):
        class EditForm(forms.Form):
            html = forms.CharField(initial=self.html,
                                   widget=forms.widgets.Textarea())
        return EditForm()

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            html = forms.CharField(widget=forms.widgets.Textarea())
        return AddForm()
    @classmethod
    def create(self,request):
        return HTMLBlock.objects.create(html=request.POST.get('html',''))

    def edit(self,vals,files):
        self.html = vals.get('html','')
        self.save()


class PullQuoteBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    body = models.TextField(blank=True)
    template_file = "pageblocks/pullquoteblock.html"
    display_name = "Pull Quote"

    def pageblock(self):
        return self.pageblocks.all()[0]


    def __unicode__(self):
        return unicode(self.pageblock())

    def edit_form(self):
        class EditForm(forms.Form):
            body = forms.CharField(widget=forms.widgets.Textarea(),
                                   initial=self.body)
        return EditForm()

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            body = forms.CharField(widget=forms.widgets.Textarea())
        return AddForm()

    @classmethod
    def create(self,request):
        return PullQuoteBlock.objects.create(body=request.POST.get('body',''))

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
    alt = models.CharField(max_length=100, null=True, blank=True)
    
    template_file = "pageblocks/imageblock.html"
    display_name = "Image Block"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def edit_form(self):
        class EditForm(forms.Form):
            image = forms.FileField(label="replace image")
            caption = forms.CharField(initial=self.caption,
                                      widget=forms.widgets.Textarea())
            alt = forms.CharField(initial=self.alt)
        return EditForm()

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            image = forms.FileField(label="select image")
            caption = forms.CharField(widget=forms.widgets.Textarea())
            alt = forms.CharField()
        return AddForm()

    @classmethod
    def create(self,request):
        if 'image' in request.FILES:
            ib = ImageBlock.objects.create(alt=request.POST.get('alt', ''),
                                           caption=request.POST.get('caption',''),
                                           image="")
            ib.save_image(request.FILES['image'])
            return ib
        return None
        

    def edit(self,vals,files):
        self.caption = vals.get('caption','')
        self.alt = vals.get('alt', '')
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
            os.makedirs(settings.MEDIA_ROOT + "/" + path)
        except:
            pass
        full_filename = path + "%s.%s" % (basename,ext)
        fd = open(settings.MEDIA_ROOT + "/" + full_filename,'wb')
        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename
        self.save()



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
    alt = models.CharField(max_length=100, null=True, blank=True)

    template_file = "pageblocks/imagepullquoteblock.html"
    display_name = "Image Pullquote"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def edit_form(self):
        class EditForm(forms.Form):
            image = forms.FileField(label="replace image")
            caption = forms.CharField(initial=self.caption,
                                      widget=forms.widgets.Textarea())
            alt = forms.CharField(initial=self.alt)
        return EditForm()

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            image = forms.FileField(label="select image")
            caption = forms.CharField(widget=forms.widgets.Textarea())
            alt = forms.CharField()
        return AddForm()

    @classmethod
    def create(self,request):
        if 'image' in request.FILES:
            ib = ImagePullQuoteBlock.objects.create(caption=request.POST.get('caption',''),
                                                    image="",
                                                    alt=request.POST.get('alt', ''))
            ib.save_image(request.FILES['image'])
            return ib
        else:
            return None

    def edit(self,vals,files):
        self.caption = vals.get('caption','')
        self.alt = vals.get('alt', '')
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
            os.makedirs(settings.MEDIA_ROOT + "/" + path)
        except:
            pass
        full_filename = path + "%s.%s" % (basename,ext)
        fd = open(settings.MEDIA_ROOT + "/" + full_filename,'wb')
        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename
        self.save()

# Using the HTMLBlockWYSIWYG
# Install tinymce into your project: http://code.google.com/p/django-tinymce/
# Override the admin/base-site.html: 
## Include: <script type="text/javascript" src="/site_media/js/tiny_mce/tiny_mce.js"></script>
## And, add the init code immediately thereafter.
# To your settings_shared.py add 'pageblocks.HTMLBlockWYSIWYG'. 
# Consider removing the generic HTMLBlock if you don't need it. Reduces confusion. 
# ./manage.py syncdb
# Define custom styles in a file called tiny_mce.css in your media/css directory
class HTMLBlockWYSIWYG(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    wysiwyg_html = models.TextField(blank=True)

    template_file = "pageblocks/htmlblock_wysiwyg.html"
    display_name = "WYSIWYG HTML Block"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())
    
    @classmethod
    def add_form(self):
        return HTMLFormWYSIWYG()
  
    def edit_form(self):
        return HTMLFormWYSIWYG(instance=self)
    
    @classmethod
    def create(self,request):
        form = HTMLFormWYSIWYG(request.POST)
        if form.is_valid():
            return form.save()

    def edit(self,vals,files):
        form = HTMLFormWYSIWYG(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()
    
class HTMLFormWYSIWYG(forms.ModelForm):
    class Meta:
        model = HTMLBlockWYSIWYG
        widgets = { 'wysiwyg_html': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'class': 'mceEditor'}), }
