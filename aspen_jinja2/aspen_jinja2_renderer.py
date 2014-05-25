"""Implement a Jinja2 renderer.

Jinja2 insists on unicode, and explicit loader objects. We assume with Jinja2
that your templates on the filesystem be encoded in UTF-8 (the result of the
template will be encoded to bytes for the wire per response.charset). We shim a
loader that returns the decoded content page and instructs Jinja2 not to
perform auto-reloading.

"""
from __future__ import absolute_import, unicode_literals
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

    For instance, if you want access to some python builtins, you might, in
    your configure-aspen.py put something like:

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

    """
    global_context = {}

    def compile(self, filepath, raw):
        environment = self.meta
        return SimplateLoader(filepath, raw).load(environment, filepath)

    def render_content(self, context):
        charset = context['response'].charset
        # Inject globally-desired context
        context.update(self.global_context)
        return self.compiled.render(context).encode(charset)


class Factory(renderers.Factory):

    Renderer = Renderer

    def compile_meta(self, configuration):
        loader = None
        if configuration.project_root is not None:
            # Instantiate a loader that will be used to resolve template bases.
            loader = FileSystemLoader(configuration.project_root)
        return Environment(loader=loader)

