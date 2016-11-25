import os
from models import TextBlock, HTMLBlock, PullQuoteBlock, SimpleImageBlock

from pagetree_export import register_class as register


@register
class Text(object):
    block_class = TextBlock
    identifier = 'text'

    def exporter(self, block, xmlfile, zipfile):
        filename = "pageblocks/%s.txt" % block.pageblock().pk
        zipfile.writestr(filename, block.body.encode("utf8"))
        print >> xmlfile, """<text src="%s" />""" % filename

    def importer(self, node, zipfile):
        children = node.getchildren()
        assert len(children) == 1 and children[0].tag == "text"
        path = children[0].get("src")
        body = zipfile.read(path)
        b = TextBlock(body=body)
        b.save()
        return b


@register
class HTML(object):
    block_class = HTMLBlock
    identifier = 'html'

    def exporter(self, block, xmlfile, zipfile):
        filename = "pageblocks/%s.html" % block.pageblock().pk
        zipfile.writestr(filename, block.html.encode("utf8"))
        print >> xmlfile, """<html src="%s" />""" % filename

    def importer(self, node, zipfile):
        children = node.getchildren()
        assert len(children) == 1 and children[0].tag == "html"
        path = children[0].get("src")
        body = zipfile.read(path)
        b = HTMLBlock(html=body)
        b.save()
        return b


@register
class PullQuote(Text):
    block_class = PullQuoteBlock
    identifier = 'pullquote'

    def importer(self, node, zipfile):
        children = node.getchildren()
        assert len(children) == 1 and children[0].tag == "text"
        path = children[0].get("src")
        body = zipfile.read(path)
        b = PullQuoteBlock(body=body)
        b.save()
        return b


# statichtml exporters


@register
class SimpleImage(object):
    block_class = SimpleImageBlock
    identifier = 'simpleimage'
    export_type = 'statichtml'

    def exporter(self, block, xmlfile, zipfile):
        filename = os.path.basename(block.image.file.name)
        filename = "pageblocks/%s-%s" % (block.pk, filename)
        zipfile.write(block.image.file.name, arcname=filename)
        return {'img_src': '/' + filename.strip('/')}
