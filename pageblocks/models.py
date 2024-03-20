from django.db import models
from pagetree.models import PageBlock
from django.conf import settings
from sorl.thumbnail.fields import ImageWithThumbnailsField
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.encoding import smart_str
from django import forms
import os
from django.template.defaultfilters import slugify
from datetime import datetime


class TextBlock(models.Model):
    pageblocks = GenericRelation(PageBlock)
    body = models.TextField(blank=True)

    template_file = "pageblocks/textblock.html"
    display_name = "Text Block"

    def __str__(self):
        return smart_str(self.pageblock())

    def pageblock(self):
        return self.pageblocks.all()[0]

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            body = forms.CharField(
                widget=forms.widgets.Textarea(attrs={'cols': 80}))
        return AddForm()

    @classmethod
    def create(self, request):
        return TextBlock.objects.create(body=request.POST.get('body', ''))

    @classmethod
    def create_from_dict(self, d):
        return TextBlock.objects.create(body=d.get('body', ''))

    def edit_form(self):
        class EditForm(forms.Form):
            body = forms.CharField(widget=forms.widgets.Textarea(),
                                   initial=self.body)
        return EditForm()

    def edit(self, vals, files):
        self.body = vals.get('body', '')
        self.save()

    def as_dict(self):
        return dict(body=self.body)

    def summary_render(self):
        if len(self.body) < 61:
            return self.body
        else:
            return self.body[:61] + "..."


class HTMLBlock(models.Model):
    pageblocks = GenericRelation(PageBlock)
    html = models.TextField(blank=True)

    template_file = "pageblocks/htmlblock.html"
    display_name = "HTML Block"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __str__(self):
        return smart_str(self.pageblock())

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
    def create(self, request):
        return HTMLBlock.objects.create(html=request.POST.get('html', ''))

    @classmethod
    def create_from_dict(self, d):
        return HTMLBlock.objects.create(html=d.get('html', ''))

    def edit(self, vals, files):
        self.html = vals.get('html', '')
        self.save()

    def as_dict(self):
        return dict(html=self.html)

    def summary_render(self):
        if len(self.html) < 61:
            return self.html.replace("<", "&lt;")
        else:
            return self.html[:61].replace("<", "&lt;") + "..."


class PullQuoteBlock(models.Model):
    pageblocks = GenericRelation(PageBlock)
    body = models.TextField(blank=True)
    template_file = "pageblocks/pullquoteblock.html"
    display_name = "Pull Quote"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __str__(self):
        return smart_str(self.pageblock())

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
    def create(self, request):
        return PullQuoteBlock.objects.create(body=request.POST.get('body', ''))

    @classmethod
    def create_from_dict(self, d):
        return PullQuoteBlock.objects.create(body=d.get('body', ''))

    def edit(self, vals, files):
        self.body = vals.get('body', '')
        self.save()

    def as_dict(self):
        return dict(body=self.body)

    def summary_render(self):
        if len(self.body) < 61:
            return self.body
        else:
            return self.body[:61] + "..."


class ImageBlock(models.Model):
    pageblocks = GenericRelation(PageBlock)
    image = ImageWithThumbnailsField(
        upload_to="images/%Y/%m/%d",
        thumbnail={
            'size': (65, 65)
        },
        extra_thumbnails={
            'admin': {
                'size': (70, 50),
                'options': ('sharpen',),
            }
        })
    caption = models.TextField(blank=True)
    alt = models.CharField(max_length=100, null=True, blank=True)
    lightbox = models.BooleanField(default=False)
    template_file = "pageblocks/imageblock.html"
    display_name = "Image Block"
    summary_template_file = "pageblocks/imageblock_summary.html"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __str__(self):
        return smart_str(self.pageblock())

    def edit_form(self):
        class EditForm(forms.Form):
            image = forms.FileField(label="replace image")
            caption = forms.CharField(initial=self.caption,
                                      widget=forms.widgets.Textarea())
            alt = forms.CharField(initial=self.alt)
            lightbox = forms.BooleanField(initial=self.lightbox)
        return EditForm()

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            image = forms.FileField(label="select image")
            caption = forms.CharField(widget=forms.widgets.Textarea())
            alt = forms.CharField()
            lightbox = forms.BooleanField()
        return AddForm()

    @classmethod
    def create(self, request):
        if 'image' in request.FILES:
            ib = ImageBlock.objects.create(
                alt=request.POST.get('alt', ''),
                caption=request.POST.get('caption', ''),
                lightbox=request.POST.get('lightbox', False),
                image="")
            ib.save_image(request.FILES['image'])
            return ib
        return None

    @classmethod
    def create_from_dict(self, d):
        # since it's coming from a dict, not a request
        # we assume that some other part is handling the writing of
        # the image file to disk and we just get a path to it
        return ImageBlock.objects.create(
            image=d.get('image', ''),
            alt=d.get('alt', ''),
            lightbox=d.get('lightbox', False),
            caption=d.get('caption', ''))

    def edit(self, vals, files):
        self.caption = vals.get('caption', '')
        self.alt = vals.get('alt', '')
        self.lightbox = vals.get('lightbox', False)
        if 'image' in files:
            self.save_image(files['image'])
        self.save()

    def save_image(self, f):
        ext = f.name.split(".")[-1].lower()
        basename = slugify(f.name.split(".")[-2].lower())[:20]
        if ext not in ['jpg', 'jpeg', 'gif', 'png']:
            # unsupported image format
            return None
        now = datetime.now()
        path = "images/%04d/%02d/%02d/" % (now.year, now.month, now.day)
        try:
            os.makedirs(settings.MEDIA_ROOT + "/" + path)
        except:
            pass
        full_filename = path + "%s.%s" % (basename, ext)
        fd = open(settings.MEDIA_ROOT + "/" + full_filename, 'wb')
        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename
        self.save()

    def as_dict(self):
        return dict(image=self.image.name,
                    alt=self.alt,
                    lightbox=self.lightbox,
                    caption=self.caption)

    def list_resources(self):
        return [self.image.url]


class ImagePullQuoteBlock(models.Model):
    pageblocks = GenericRelation(PageBlock)
    image = ImageWithThumbnailsField(
        upload_to="images/%Y/%m/%d",
        thumbnail={
            'size': (65, 65)
        },
        extra_thumbnails={
            'admin': {
                'size': (70, 50),
                'options': ('sharpen', ),
            }
        })
    caption = models.TextField(blank=True)
    alt = models.CharField(max_length=100, null=True, blank=True)

    template_file = "pageblocks/imagepullquoteblock.html"
    summary_template_file = "pageblocks/imagepullquoteblock_summary.html"
    display_name = "Image Pullquote"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __str__(self):
        return smart_str(self.pageblock())

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
    def create(self, request):
        if 'image' in request.FILES:
            ib = ImagePullQuoteBlock.objects.create(
                caption=request.POST.get('caption', ''),
                image="",
                alt=request.POST.get('alt', ''))
            ib.save_image(request.FILES['image'])
            return ib
        else:
            return None

    @classmethod
    def create_from_dict(self, d):
        # since it's coming from a dict, not a request
        # we assume that some other part is handling the writing of
        # the image file to disk and we just get a path to it
        return ImagePullQuoteBlock.objects.create(
            image=d.get('image', ''),
            alt=d.get('alt', ''),
            caption=d.get('caption', ''))

    def edit(self, vals, files):
        self.caption = vals.get('caption', '')
        self.alt = vals.get('alt', '')
        if 'image' in files:
            self.save_image(files['image'])
        self.save()

    def save_image(self, f):
        ext = f.name.split(".")[-1].lower()
        basename = slugify(f.name.split(".")[-2].lower())[:20]
        if ext not in ['jpg', 'jpeg', 'gif', 'png']:
            # unsupported image format
            return None
        now = datetime.now()
        path = "images/%04d/%02d/%02d/" % (now.year, now.month, now.day)
        try:
            os.makedirs(settings.MEDIA_ROOT + "/" + path)
        except:
            pass
        full_filename = path + "%s.%s" % (basename, ext)
        fd = open(settings.MEDIA_ROOT + "/" + full_filename, 'wb')
        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename
        self.save()

    def as_dict(self):
        return dict(image=self.image.name,
                    alt=self.alt,
                    caption=self.caption)

    def list_resources(self):
        return [self.image.url]


# Using the HTMLBlockWYSIWYG
# Install tinymce into your project: http://code.google.com/p/django-tinymce/
# Override the admin/base-site.html:
## Include: <script type="text/javascript"
##          src="/site_media/js/tiny_mce/tiny_mce.js"></script>
## And, add the init code immediately thereafter.
# To your settings_shared.py add 'pageblocks.HTMLBlockWYSIWYG'.
# Consider removing the generic HTMLBlock if you don't need it.
#  Reduces confusion.
# ./manage.py syncdb
# Define custom styles in a file called tiny_mce.css
# in your media/css directory
class HTMLBlockWYSIWYG(models.Model):
    pageblocks = GenericRelation(PageBlock)
    wysiwyg_html = models.TextField(blank=True)

    template_file = "pageblocks/htmlblock_wysiwyg.html"
    display_name = "WYSIWYG HTML Block"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __str__(self):
        return smart_str(self.pageblock())

    @classmethod
    def add_form(self):
        return HTMLFormWYSIWYG()

    def edit_form(self):
        return HTMLFormWYSIWYG(instance=self)

    @classmethod
    def create(self, request):
        form = HTMLFormWYSIWYG(request.POST)
        if form.is_valid():
            return form.save()

    @classmethod
    def create_from_dict(self, d):
        return HTMLBlockWYSIWYG.objects.create(
            wysiwyg_html=d.get('wysiwyg_html', ''))

    def edit(self, vals, files):
        form = HTMLFormWYSIWYG(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def as_dict(self):
        return dict(wysiwyg_html=self.wysiwyg_html)


class HTMLFormWYSIWYG(forms.ModelForm):
    class Meta:
        model = HTMLBlockWYSIWYG
        widgets = {
            'wysiwyg_html': forms.Textarea(
                attrs={'cols': 80, 'rows': 20, 'class': 'mceEditor'}),
        }
        exclude = []
