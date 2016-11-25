from django.db import models
from django.conf import settings
from django import forms
from django.template.defaultfilters import slugify
from pagetree.generic.models import BasePageBlock


class TextBlock(BasePageBlock):
    body = models.TextField(blank=True)

    template_file = "pageblocks/textblock.html"
    display_name = "Text Block"

    @classmethod
    def add_form(cls):
        class AddForm(forms.Form):
            body = forms.CharField(
                widget=forms.widgets.Textarea(attrs={'cols': 80}))
        return AddForm()

    @classmethod
    def create(cls, request):
        return cls.objects.create(body=request.POST.get('body', ''))

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create(body=d.get('body', ''))

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


class HTMLBlock(BasePageBlock):
    html = models.TextField(blank=True)

    template_file = "pageblocks/htmlblock.html"
    display_name = "HTML Block"

    def edit_form(self):
        class EditForm(forms.Form):
            html = forms.CharField(initial=self.html,
                                   widget=forms.widgets.Textarea())
        return EditForm()

    @classmethod
    def add_form(cls):
        class AddForm(forms.Form):
            html = forms.CharField(widget=forms.widgets.Textarea())
        return AddForm()

    @classmethod
    def create(cls, request):
        return cls.objects.create(html=request.POST.get('html', ''))

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create(html=d.get('html', ''))

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


class PullQuoteBlock(BasePageBlock):
    body = models.TextField(blank=True)
    template_file = "pageblocks/pullquoteblock.html"
    display_name = "Pull Quote"

    def edit_form(self):
        class EditForm(forms.Form):
            body = forms.CharField(widget=forms.widgets.Textarea(),
                                   initial=self.body)
        return EditForm()

    @classmethod
    def add_form(cls):
        class AddForm(forms.Form):
            body = forms.CharField(widget=forms.widgets.Textarea())
        return AddForm()

    @classmethod
    def create(cls, request):
        return cls.objects.create(body=request.POST.get('body', ''))

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create(body=d.get('body', ''))

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


class SimpleImageBlock(BasePageBlock):
    """
    SimpleImageBlock is ImageBlock without the automatic
    thumbnailing functionality.
    """
    image = models.ImageField(upload_to="images")
    caption = models.TextField(blank=True)
    alt = models.CharField(max_length=100, null=True, blank=True)
    template_file = "pageblocks/simpleimageblock.html"
    display_name = "Simple Image Block"

    def edit_form(self):
        class EditForm(forms.Form):
            image = forms.FileField(label="replace image")
            caption = forms.CharField(initial=self.caption,
                                      required=False,
                                      widget=forms.widgets.Textarea())
            alt = forms.CharField(initial=self.alt, required=False)
        return EditForm()

    @classmethod
    def add_form(cls):
        class AddForm(forms.Form):
            image = forms.FileField(label="select image")
            caption = forms.CharField(widget=forms.widgets.Textarea(),
                                      required=False)
            alt = forms.CharField(required=False)
        return AddForm()

    @classmethod
    def create(cls, request):
        if 'image' in request.FILES:
            ib = cls.objects.create(
                alt=request.POST.get('alt', ''),
                caption=request.POST.get('caption', ''),
                image="")
            ib.save_image(request.FILES['image'])
            return ib
        return None

    @classmethod
    def create_from_dict(cls, d):
        # since it's coming from a dict, not a request
        # we assume that some other part is handling the writing of
        # the image file to disk and we just get a path to it
        return cls.objects.create(
            image=d.get('image', ''),
            alt=d.get('alt', ''),
            caption=d.get('caption', ''))

    def as_dict(self):
        return dict(image=self.image.name,
                    alt=self.alt,
                    caption=self.caption)

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
        full_filename = "%s/%s.%s" % (
            self.image.field.upload_to, basename, ext)
        fd = self.image.storage.open(
            settings.MEDIA_ROOT + "/" + full_filename, 'wb')

        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename
        self.save()


# Using the HTMLBlockWYSIWYG
# Install tinymce into your project: http://code.google.com/p/django-tinymce/
# Override the admin/base-site.html:
# Include: <script type="text/javascript"
#          src="/site_media/js/tiny_mce/tiny_mce.js"></script>
# And, add the init code immediately thereafter.
# To your settings_shared.py add 'pageblocks.HTMLBlockWYSIWYG'.
# Consider removing the generic HTMLBlock if you don't need it.
#  Reduces confusion.
# ./manage.py syncdb
# Define custom styles in a file called tiny_mce.css
# in your media/css directory
class HTMLBlockWYSIWYG(BasePageBlock):
    wysiwyg_html = models.TextField(blank=True)

    template_file = "pageblocks/htmlblock_wysiwyg.html"
    display_name = "WYSIWYG HTML Block"

    @classmethod
    def add_form(cls):
        return HTMLFormWYSIWYG()

    def edit_form(self):
        return HTMLFormWYSIWYG(instance=self)

    @classmethod
    def create(cls, request):
        form = HTMLFormWYSIWYG(request.POST)
        if form.is_valid():
            return form.save()

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create(
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
        fields = '__all__'
        widgets = {
            'wysiwyg_html': forms.Textarea(
                attrs={'cols': 80, 'rows': 20, 'class': 'mceEditor'}),
        }
