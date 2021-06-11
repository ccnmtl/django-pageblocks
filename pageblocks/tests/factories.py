import factory
from factory.fuzzy import FuzzyText

from pageblocks.models import (
    TextBlock, HTMLBlock, PullQuoteBlock,
    SimpleImageBlock, HTMLBlockWYSIWYG
)


class TextBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TextBlock

    body = FuzzyText()


class HTMLBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HTMLBlock

    html = FuzzyText()


class PullQuoteBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PullQuoteBlock

    body = FuzzyText()


class SimpleImageBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SimpleImageBlock

    image = factory.django.ImageField()
    caption = FuzzyText()


class HTMLBlockWYSIWYGFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HTMLBlockWYSIWYG

    wysiwyg_html = FuzzyText()
