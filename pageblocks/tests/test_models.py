from django.test import TestCase
from pageblocks.models import TextBlock, HTMLBlock, PullQuoteBlock, ImageBlock
from pageblocks.models import ImagePullQuoteBlock, HTMLBlockWYSIWYG


class TextBlockTest(TestCase):
    def test_add_form(self):
        f = TextBlock.add_form()
        self.assertTrue('body' in f.fields)

    def test_create_from_dict(self):
        d = dict(body='foo')
        tb = TextBlock.create_from_dict(d)
        self.assertEqual(tb.body, 'foo')

    def test_edit_form(self):
        tb = TextBlock.objects.create(body='foo')
        f = tb.edit_form()
        self.assertTrue('body' in f.fields)

    def test_edit(self):
        tb = TextBlock.objects.create(body='foo')
        tb.edit(dict(body='bar'), None)
        self.assertEqual(tb.body, 'bar')

    def test_as_dict(self):
        tb = TextBlock.objects.create(body='foo')
        self.assertEqual(tb.as_dict(), dict(body='foo'))

    def test_summary_render_short(self):
        tb = TextBlock.objects.create(body='foo')
        self.assertEqual(tb.summary_render(), 'foo')

    def test_summary_render_long(self):
        tb = TextBlock.objects.create(body='foo' * 30)
        self.assertTrue(tb.summary_render().endswith("..."))
        self.assertEqual(len(tb.summary_render()), 64)


class HTMLBlockTest(TestCase):
    def test_add_form(self):
        f = HTMLBlock.add_form()
        self.assertTrue('html' in f.fields)

    def test_create_from_dict(self):
        d = dict(html='foo')
        tb = HTMLBlock.create_from_dict(d)
        self.assertEqual(tb.html, 'foo')

    def test_edit_form(self):
        tb = HTMLBlock.objects.create(html='foo')
        f = tb.edit_form()
        self.assertTrue('html' in f.fields)

    def test_edit(self):
        tb = HTMLBlock.objects.create(html='foo')
        tb.edit(dict(html='bar'), None)
        self.assertEqual(tb.html, 'bar')

    def test_as_dict(self):
        tb = HTMLBlock.objects.create(html='foo')
        self.assertEqual(tb.as_dict(), dict(html='foo'))

    def test_summary_render_short(self):
        tb = HTMLBlock.objects.create(html='foo')
        self.assertEqual(tb.summary_render(), 'foo')

    def test_summary_render_long(self):
        tb = HTMLBlock.objects.create(html='foo' * 30)
        self.assertTrue(tb.summary_render().endswith("..."))
        self.assertEqual(len(tb.summary_render()), 64)


class PullQuoteBlockTest(TestCase):
    def test_add_form(self):
        f = PullQuoteBlock.add_form()
        self.assertTrue('body' in f.fields)

    def test_create_from_dict(self):
        d = dict(body='foo')
        tb = PullQuoteBlock.create_from_dict(d)
        self.assertEqual(tb.body, 'foo')

    def test_edit_form(self):
        tb = PullQuoteBlock.objects.create(body='foo')
        f = tb.edit_form()
        self.assertTrue('body' in f.fields)

    def test_edit(self):
        tb = PullQuoteBlock.objects.create(body='foo')
        tb.edit(dict(body='bar'), None)
        self.assertEqual(tb.body, 'bar')

    def test_as_dict(self):
        tb = PullQuoteBlock.objects.create(body='foo')
        self.assertEqual(tb.as_dict(), dict(body='foo'))

    def test_summary_render_short(self):
        tb = PullQuoteBlock.objects.create(body='foo')
        self.assertEqual(tb.summary_render(), 'foo')

    def test_summary_render_long(self):
        tb = PullQuoteBlock.objects.create(body='foo' * 30)
        self.assertTrue(tb.summary_render().endswith("..."))
        self.assertEqual(len(tb.summary_render()), 64)


class ImageBlockTest(TestCase):
    def test_add_form(self):
        f = ImageBlock.add_form()
        self.assertTrue('image' in f.fields)
        self.assertTrue('caption' in f.fields)
        self.assertTrue('alt' in f.fields)
        self.assertTrue('lightbox' in f.fields)

    def test_create_from_dict(self):
        d = dict(image='foo/bar/blah.jpg')
        tb = ImageBlock.create_from_dict(d)
        self.assertEqual(tb.image, 'foo/bar/blah.jpg')
        self.assertEqual(tb.caption, '')

    def test_edit_form(self):
        tb = ImageBlock.create_from_dict(dict(image='foo/bar/blah.jpg'))
        f = tb.edit_form()
        self.assertTrue('caption' in f.fields)

    def test_edit(self):
        tb = ImageBlock.create_from_dict(dict(image='foo/bar/blah.jpg'))
        tb.edit(dict(image='foo/bar/blah.jpg', caption='bar'), [])
        self.assertEqual(tb.caption, 'bar')

    def test_as_dict(self):
        tb = ImageBlock.create_from_dict(dict(image='foo/bar/blah.jpg'))
        self.assertEqual(
            tb.as_dict(),
            dict(image='foo/bar/blah.jpg',
                 alt='', caption='', lightbox=False))

    def test_list_resources(self):
        tb = ImageBlock.create_from_dict(dict(image='foo/bar/blah.jpg'))
        self.assertEqual(tb.list_resources(), ['foo/bar/blah.jpg'])


class ImagePullQuoteBlockTest(TestCase):
    def test_add_form(self):
        f = ImagePullQuoteBlock.add_form()
        self.assertTrue('image' in f.fields)
        self.assertTrue('caption' in f.fields)
        self.assertTrue('alt' in f.fields)

    def test_create_from_dict(self):
        d = dict(image='foo/bar/blah.jpg')
        tb = ImagePullQuoteBlock.create_from_dict(d)
        self.assertEqual(tb.image, 'foo/bar/blah.jpg')
        self.assertEqual(tb.caption, '')

    def test_edit_form(self):
        tb = ImagePullQuoteBlock.create_from_dict(
            dict(image='foo/bar/blah.jpg'))
        f = tb.edit_form()
        self.assertTrue('caption' in f.fields)

    def test_edit(self):
        tb = ImagePullQuoteBlock.create_from_dict(
            dict(image='foo/bar/blah.jpg'))
        tb.edit(dict(image='foo/bar/blah.jpg', caption='bar'), [])
        self.assertEqual(tb.caption, 'bar')

    def test_as_dict(self):
        tb = ImagePullQuoteBlock.create_from_dict(
            dict(image='foo/bar/blah.jpg'))
        self.assertEqual(
            tb.as_dict(),
            dict(image='foo/bar/blah.jpg',
                 alt='', caption=''))

    def test_list_resources(self):
        tb = ImagePullQuoteBlock.create_from_dict(
            dict(image='foo/bar/blah.jpg'))
        self.assertEqual(tb.list_resources(), ['foo/bar/blah.jpg'])


class HTMLBlockWYSIWYGTest (TestCase):
    def test_add_form(self):
        f = HTMLBlockWYSIWYG.add_form()
        self.assertTrue('wysiwyg_html' in f.fields)

    def test_create_from_dict(self):
        d = dict(wysiwyg_html='foo')
        tb = HTMLBlockWYSIWYG.create_from_dict(d)
        self.assertEqual(tb.wysiwyg_html, 'foo')

    def test_edit_form(self):
        tb = HTMLBlockWYSIWYG.objects.create(wysiwyg_html='foo')
        f = tb.edit_form()
        self.assertTrue('wysiwyg_html' in f.fields)

    def test_edit(self):
        tb = HTMLBlockWYSIWYG.objects.create(wysiwyg_html='foo')
        tb.edit(dict(wysiwyg_html='bar'), None)
        self.assertEqual(tb.wysiwyg_html, 'bar')

    def test_as_dict(self):
        tb = HTMLBlockWYSIWYG.objects.create(wysiwyg_html='foo')
        self.assertEqual(tb.as_dict(), dict(wysiwyg_html='foo'))
