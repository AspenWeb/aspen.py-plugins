"""Implement a Jinja2 renderer.

Jinja2 insists on unicode, and explicit loader objects. We assume with Jinja2
that your templates on the filesystem are encoded in UTF-8. We shim a loader
that returns the decoded content page and instructs Jinja2 not to perform
auto-reloading.

"""
from __future__ import absolute_import, unicode_literals

import re

from aspen import renderers
from jinja2 import BaseLoader, Environment, FileSystemLoader


class SimplateLoader(BaseLoader):
    """Jinja2 really wants to get templates via a Loader object.

    See: http://jinja.pocoo.org/docs/api/#loaders

    """

    def __init__(self, filepath, raw):
        self.filepath = filepath
        self.decoded = raw

    def get_source(self, environment, template):
        return self.decoded, self.filepath, True


class Renderer(renderers.Renderer):
    """Renderer for jinja2 templates.

    Jinja2 is sandboxed, so only gets the context from simplate, not even
    access to python builtins.  Put any global functions or variables you
    want access to in your template into the 'global_context' here to have
    it passed along, augmented, of course, by the actual local context.

    For instance, if you want access to some python builtins, you might do:

        website.renderer_factories['jinja2'].Renderer.global_context = {
            'range': range,
            'unicode': unicode,
            'enumerate': enumerate,
            'len': len,
            'float': float,
            'type': type
        }

    Clearly, by doing so, you're overriding jinja's explicit decision to not
    include those things by default, which may be fraught - but that's up to
    you.

    By default Jinja's `autoescape` is turned off, you can enable it by setting

        website.renderer_factories['jinja2'].Renderer.autoescape = True

    This will only turn on Jinja's autoescape when rendering an HTML or XML
    page (precisely, any media type that matches the `Renderer.sgml_type_re`
    regular expression).

    """
    autoescape = False
    global_context = {}
    sgml_type_re = re.compile(r'\b(ht|sg|x)ml\b')

    def compile(self, filepath, raw):
        self.is_sgml = bool(self.sgml_type_re.search(self.media_type))
        if self.autoescape and self.is_sgml:
            environment = self.meta['htmlescaped_env']
        else:
            environment = self.meta['default_env']
        return SimplateLoader(filepath, raw).load(environment, filepath)

    def render_content(self, context):
        # Inject globally-desired context
        context.update(self.global_context)
        return self.compiled.render(context)


class Factory(renderers.Factory):

    Renderer = Renderer

    def compile_meta(self, configuration):
        loader = None
        if configuration.project_root is not None:
            # Instantiate a loader that will be used to resolve template bases.
            loader = FileSystemLoader(configuration.project_root)
        return {
            'default_env': Environment(loader=loader),
            'htmlescaped_env': Environment(loader=loader, autoescape=True),
        }

