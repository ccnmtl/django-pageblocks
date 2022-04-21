from django import forms
from django.forms import widgets


class AddTextBlockForm(forms.Form):
    label = forms.CharField()
    body = forms.CharField(widget=widgets.Textarea(attrs={'cols': 80}))


class AddImageBlockForm(forms.Form):
    label = forms.CharField()
    image = forms.ImageField()
    caption = forms.CharField(widget=widgets.Textarea(attrs={'cols': 80}))


class AddHTMLBlockForm(forms.Form):
    label = forms.CharField()
    html = forms.CharField(widget=widgets.Textarea(attrs={'cols': 80}))


class AddImagePullQuoteBlockForm(forms.Form):
    label = forms.CharField()
    image = forms.ImageField()
    caption = forms.CharField(widget=widgets.Textarea(attrs={'cols': 80}))
