import factory
from factory.fuzzy import FuzzyText

from pageblocks.models import (
    TextBlock, HTMLBlock, PullQuoteBlock,
    SimpleImageBlock, HTMLBlockWYSIWYG
)


class TextBlockFactory(factory.DjangoModelFactory):
    class Meta:
        model = TextBlock

    body = FuzzyText()


class HTMLBlockFactory(factory.DjangoModelFactory):
    class Meta:
        model = HTMLBlock

    html = FuzzyText()


class PullQuoteBlockFactory(factory.DjangoModelFactory):
    class Meta:
        model = PullQuoteBlock

    body = FuzzyText()


class SimpleImageBlockFactory(factory.DjangoModelFactory):
    class Meta:
        model = SimpleImageBlock

    image = factory.django.ImageField()
    caption = FuzzyText()


class HTMLBlockWYSIWYGFactory(factory.DjangoModelFactory):
    class Meta:
        model = HTMLBlockWYSIWYG

    wysiwyg_html = FuzzyText()
